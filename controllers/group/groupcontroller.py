"""
Group controller for Flask API
Handles inbound request regarding groups
"""

from controllers.core import AbstractController
from controllers.group.resources import NewGroupResource


class GroupController(AbstractController):
    def add_resources(self):
        self.api.add_resource(NewGroupResource, "/groups/new")
