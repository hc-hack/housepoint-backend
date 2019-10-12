"""
Flask_RESTful resources for account creation
"""

from flask_restful import Resource, reqparse
from flask import Request
from models.account import AccountModel
import re

_model = AccountModel()


class AccountResource(Resource):
    def __init__(self):
        super().__init__()
        self.model = _model

    # TODO: Authentication on this endpoint(!)
    def get(self, account_id):
        account = self.model.find_by_id(account_id)
        if not account:
            return {
                "message": "Account not found"
            }, 404

        del account["password"]
        return account

    def delete(self, account_id):
        success, account = self.model.delete_by_id(account_id)
        if not account:
            return {
                "message": "Account not found"
            }, 404
        if success:
            return {
                "message": "Successfully deleted account"
            }
        return {
            "message": "Failed to delete account"
        }, 500


class AccountCreationResource(Resource):
    def __init__(self):
        super().__init__()
        self.model = _model
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("first_name")
        self.parser.add_argument("last_name")
        self.parser.add_argument("username")
        self.parser.add_argument("email")
        self.parser.add_argument("password")

    def post(self):
        """
        Account creation endpoint
        """
        account_object = self.parser.parse_args()
        is_valid, reason = self._validate(account_object)
        if not is_valid:
            return {
                "message": "Invalid account details supplied",
                "reason": reason
            }, 400

        success, user_id = self.model.add_user(account_object)
        if success:
            return {
                "message": "Successfully inserted user",
                "user_id": user_id
            }, 200

        return {
            "message": "Failed to insert new user"
        }, 500

    def _validate(self, account_object):
        """
        Perform some simple validation on the provided
        account object
        """
        first_name = account_object.get("first_name")
        last_name = account_object.get("last_name")
        username = account_object.get("username").lower()
        email = account_object.get("email")
        password = account_object.get("password")

        if not first_name or not last_name or not username or not email or not password:
            return False, "Fields missing from POST body"

        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', email):
            return False, "Invalid email"

        # Quick checks passed, check in DB for existing user
        account = self.model.find_user(
            username=username, email=email, exclusive=False)

        if account:
            return False, "Account Exists"
        return True, None


class AccountLoginResource(Resource):
    def __init__(self):
        self.model = _model
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username")
        self.parser.add_argument("password")

    def post(self):
        login_details = self.parser.parse_args()
        # FIXME: Proper display_name and username handling
        username = login_details.get("username").lower()
        password = login_details.get("password")
        if not username or not password:
            return {
                "message": "Username and password is required in POST body"
            }, 400

        # TODO: Make a JWT!
        authenticated, account = self.model.authenticate(username, password)
        if authenticated:
            del account["password"]
            return {
                "message": "Successfully authenticated",
                "account": account
            }
        return {
            "message": "Failed to authenticate"
        }, 401
