import json
import requests
import logging
from api.errors import *
from flask import request
from flask_restful import Resource

# Hatchways Server Endpoint
EXTERNAL_SERVER_ENDPOINT = 'https://api.hatchways.io/assessment/blog/posts'

# Valid tag parameters
SORT_BY_OPTIONS = ["id", "reads", "likes", "popularity"]
SORTING_ORDER = ["asc", "desc"]


# Blog Resource
class Blog(Resource):

    def get(self):
        tags_string = request.args.get("tags", None, str)
        sort_by_param = request.args.get("sortBy", "id")  # id is default
        post_sorting_order = request.args.get("direction", "asc")  # Ascending order by default

        if tags_string is None:
            return no_tag_error, 400

        if sort_by_param not in SORT_BY_OPTIONS:
            return wrong_sortby_input_error, 400

        if post_sorting_order not in SORTING_ORDER:
            return sorting_order_error, 400

        clean_tags = tags_string.strip().lower().split(",")

        try:
            posts = self.__get_posts(clean_tags)
            sorted_post_list = self.__sort_posts(posts, sort_by_param, post_sorting_order)
            final_resp_obj = {"posts": sorted_post_list}
            logging.debug("Works!")
            return final_resp_obj, 200

        except Exception as e:
            logging.error(str(e))
            return external_server_error, 503

    def post(self):
        return {'success': False, 'message': 'POST Not Allowed'}, 405

    def __get_posts(self, params):
        posts = list()
        unique_set = set()
        for tag in params:
            payload = {'tag': str(tag)}
            current_tag_resp = requests.get(EXTERNAL_SERVER_ENDPOINT, params=payload).json()
            if "posts" in current_tag_resp:
                self.__parse_each_post(current_tag_resp, posts, unique_set)
            else:
                logging.error(str("No Posts for the tag" + str(tag)))
        return posts

    def __parse_each_post(self, current_tag_resp, posts, unique_set):
        for each_post in current_tag_resp["posts"]:
            current_post_json_dmp = json.dumps(each_post)
            if current_post_json_dmp not in unique_set:
                posts.append(each_post)
                unique_set.add(current_post_json_dmp)

    def __sort_posts(self, post_list, sort_by, ordering):
        is_reverse = False
        if ordering == "desc":
            is_reverse = True
        sorted_post_list = sorted(post_list, key=lambda post: post[sort_by], reverse=is_reverse)
        return sorted_post_list
