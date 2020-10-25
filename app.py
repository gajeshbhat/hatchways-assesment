import json
import requests
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

# Errors
no_tag_error = {"error": "Tags parameter is required"}
wrong_sortby_input_error = {"error": "sortBy parameter is invalid"}
sorting_order_error = {"error": "soring order not provided"}
external_server_error = {"error": "External Server did not respond. Try Again later."}

# Hatchways Server Link
EXTERNAL_SERVER_ENDPOINT = 'https://api.hatchways.io/assessment/blog/posts'


# Ping Resource
class Ping(Resource):

    def get(self):
        return {'success': True}, 200

    def post(self):
        return {'success': False}, 404


# Blog Resource
class Blog(Resource):

    def get(self):
        tags_string = request.args.get("tags", None, str)

        if tags_string is None:
            return no_tag_error, 400

        sortby_str = request.args.get("sortBy", "id")

        if sortby_str not in ["id", "reads", "likes", "popularity"]:
            return wrong_sortby_input_error, 400

        post_sorting_order = request.args.get("direction", "asc")
        if post_sorting_order not in ["asc", "desc"]:
            return sorting_order_error, 400

        clean_tags = tags_string.strip().lower().split(",")

        try:
            # Request Hatchways Server for data
            posts = list()
            unique_set = set()
            for tag in clean_tags:
                payload = {'tag': str(tag)}
                current_tag_resp = requests.get(EXTERNAL_SERVER_ENDPOINT, params=payload).json()

                if "posts" in current_tag_resp:
                    for each_post in current_tag_resp["posts"]:
                        current_post_json_dmp = json.dumps(each_post)
                        if current_post_json_dmp not in unique_set:
                            posts.append(each_post)
                            unique_set.add(current_post_json_dmp)
                else:
                    return external_server_error, 400

            # Sort in-place based on passed parameter
            is_reverse = True if post_sorting_order == "desc" else False
            sorted_post_list = sorted(posts, key=lambda post: post[sortby_str], reverse=is_reverse)

            final_resp_obj = {"posts": sorted_post_list}

            return final_resp_obj, 200

        except Exception as e:
            print(e.with_traceback())
            return external_server_error, 400

    def post(self):
        return {'success': False}, 404


# Add API Resources
api.add_resource(Ping, '/api/ping')
api.add_resource(Blog, '/api/posts')

if __name__ == '__main__':
    app.run()
