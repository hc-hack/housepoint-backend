"""
Account controller for Flask API
Handles inbound requests regarding accounts
"""

from controllers.core import AbstractController
from flask_restful import Resource
from controllers.account.resources import AccountResource, AccountCreationResource


class AccountController(AbstractController):
    def add_resources(self):
        self.api.add_resource(AccountResource, "/account/<string:account_id>")
        self.api.add_resource(AccountCreationResource, "/account/create")
