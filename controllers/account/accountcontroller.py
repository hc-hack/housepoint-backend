"""
Account controller for Flask API
Handles inbound requests regarding accounts
"""

from controllers.core import AbstractController
from controllers.account.resources import AccountResource, AccountCreationResource, AccountLoginResource


class AccountController(AbstractController):
    def add_resources(self):
        self.api.add_resource(AccountResource, "/account/<string:account_id>")
        self.api.add_resource(AccountCreationResource, "/account/create")
        self.api.add_resource(AccountLoginResource, "/account/login")
