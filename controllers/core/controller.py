"""
Base controller classes and methods
"""

from abc import ABCMeta


class AbstractController():
    """ Abstract Flask controller """

    __metaclass__ = ABCMeta

    def __init__(self, flask, api):
        # Bind the Flask and Flask_RESTful instances
        self.flask = flask
        self.api = api
        self.add_resources()

    def add_resources(self):
        pass

    def bind(self, flask, api):
        """
        Bind the Flask and Flask_RESTful objects to the local class
        """
        self.flask = flask
        self.api = api

    def register_routes(self):
        """
        Abstract Register Routes function
        """
        raise NotImplementedError()
