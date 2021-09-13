import logging
from flask import Flask
from flask_restful import Api
from api import ping
from api import blog

# Initialize App
app = Flask(__name__)

# Initialize API App
api = Api(app)

# Add API Resources
api.add_resource(ping.Ping, '/api/ping')
api.add_resource(blog.Blog, '/api/posts')

if __name__ == '__main__':
    app.run()
