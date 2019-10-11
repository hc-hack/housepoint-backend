"""
register.py

Holds the routes and handler classes
"""
from controllers.account import AccountController


def register_routes(flask, api):
    """ Bind the routes to the Flask object """
    AccountController(flask, api)
