"""
Flask_RESTful resources for account creation
"""

from flask_restful import Resource, reqparse
from models.group import GroupModel

# _model = GroupModel()


class NewGroupResource(Resource):
    def __init__(self):
        super().__init__()
        # self.model = _model
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str)
        self.parser.add_argument("private", type=bool)

    def post(self):
        args = self.parser.parse_args()
        name = args.get("name")
        private = args.get("private")
        if not name or private is None:
            return {
                "message": "Name and private are both required"
            }, 400

        return args
