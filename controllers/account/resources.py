"""
Flask_RESTful resources for account creation
"""

from flask_restful import Resource, reqparse
from flask import Request


class AccountResource(Resource):
    def get(self, account_id):
        return account_id


class AccountCreationResource(Resource):
    def __init__(self):
        super().__init__()
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
        is_valid = self._validate(account_object)

    @staticmethod
    def _validate(account_object) -> bool:
        return True
