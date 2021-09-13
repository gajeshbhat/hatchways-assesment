import logging
from flask import Flask
from flask_restful import Api
from api import ping
from api import blog
from flasgger import Swagger

# Initialize App
app = Flask(__name__)

# Configure Swagger
app.config['SWAGGER'] = {
    'title': 'Hatchways Test',
    'uiversion': 2
}

# Custom Config to change Swagger UI Path
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/"
}

swag_app = Swagger(app,config=swagger_config)

# Initialize API App
api = Api(app)

# Add API Resources
api.add_resource(ping.Ping, '/api/ping')
api.add_resource(blog.Blog, '/api/posts')

if __name__ == '__main__':
    app.run()
