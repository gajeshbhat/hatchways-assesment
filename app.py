import logging
from flask import Flask
from flask_restful import Api
from api.ping import Ping
from api.blog import Blog
from api.logs import ApiLogs

# Initialize App
app = Flask(__name__)

# Initialize API App
api = Api(app)

# Add API Resources
api.add_resource(Ping, '/api/ping')
api.add_resource(Blog, '/api/posts')


# Add Log Endpoint for Devs
# api.add_resource(ApiLogs, '/api/dev/logs', resource_class_kwargs={
#     'logger': logging.
# })

if __name__ == '__main__':
    app.run()
