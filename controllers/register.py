"""
register.py

Holds the routes and handler classes
"""
from controllers.account import AccountController
from controllers.group import GroupController


def register_routes(flask, api):
    """ Bind the routes to the Flask object """
    AccountController(flask, api)
    GroupController(flask, api)
