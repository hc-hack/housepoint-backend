from flask import Flask
from controllers import register_routes
from flask_restful import Api


class HousepointApplication():
    def __init__(self):
        """ Initialise the application """
        self.flask = Flask(__name__)
        self.api = Api(self.flask)
        self.register_controller()

    def register_controller(self):
        """ Register the controllers each namespace """
        register_routes(self.flask, self.api)

    def run(self):
        """ Run the flask app as debug """
        self.flask.run(debug=True)


if __name__ == "__main__":
    app = HousepointApplication()
    app.run()
