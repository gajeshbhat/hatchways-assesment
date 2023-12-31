import json
import threading

import requests
import logging
from api.errors import *
from flask import request
from flask_restful import Resource
from functools import lru_cache
from api.status_codes import SUCCESSFUL_OK,BAD_REQUEST, METHOD_NOT_ALLOWED

# Hatchways Server Endpoint
EXTERNAL_SERVER_ENDPOINT = 'https://api.hatchways.io/assessment/blog/posts'

# Valid tag parameters
SORT_BY_OPTIONS = ["id", "reads", "likes", "popularity"]
SORTING_ORDER = ["asc", "desc"]

# Cache Max Size
MAX_CACHE_SIZE = 128


# Blog Resource
class Blog(Resource):

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    # @lru_cache is not ideal for Multiple workers for frameworks that use gunicorn, If given time I would use a a
    # central cache store like memcached to avoid misses. More :
    # https://krzysztofzuraw.com/blog/2017/gunicorn-lru-cache-pitfall
    def get(self):
        tags_string = request.args.get("tags", None, str)
        sort_by_param = request.args.get("sortBy", "id")  # id is default
        post_sorting_order = request.args.get("direction", "asc")  # Ascending order by default

        if tags_string is None:
            return no_tag_error, BAD_REQUEST

        if sort_by_param not in SORT_BY_OPTIONS:
            return wrong_sortby_input_error, BAD_REQUEST

        if post_sorting_order not in SORTING_ORDER:
            return sorting_order_error, BAD_REQUEST

        clean_tags = tags_string.strip().lower().split(",")

        try:
            posts = self.__get_posts(clean_tags)
            sorted_post_list = self.__sort_posts(posts, sort_by_param, post_sorting_order)
            final_resp_obj = {"posts": sorted_post_list}
            return final_resp_obj, SUCCESSFUL_OK

        except Exception as e:
            logging.error(str(e))
            return external_server_error, BAD_REQUEST

    def post(self):
        return json.dumps({'success': False, 'message': 'POST Not Allowed'}), METHOD_NOT_ALLOWED

    # Private helper method to get posts
    def __get_posts(self, params):
        request_threads = list()
        posts = list()
        unique_set = set()
        for tag in params:
            each_tag_thread = threading.Thread(target=self.__process_tag,
                                               args=(tag, posts, unique_set))
            each_tag_thread.start()
            request_threads.append(each_tag_thread)
        # Wait for threads to complete processing requests
        for thread in request_threads:
            thread.join()

        return posts

    # Private helper method that runs on independent thread and makes concurrent requests
    def __process_tag(self, tag, posts, unique_set):
        payload = {'tag': str(tag)}
        current_tag_resp = requests.get(EXTERNAL_SERVER_ENDPOINT, params=payload).json()
        if "posts" in current_tag_resp:
            self.__parse_each_post(current_tag_resp, posts, unique_set)
        else:
            logging.error(str("No Posts for the tag" + str(tag)))

    # Private helper method to parse each post
    def __parse_each_post(self, current_tag_resp, posts, unique_set):
        for each_post in current_tag_resp["posts"]:
            current_post_json_dmp = json.dumps(each_post)
            if current_post_json_dmp not in unique_set:
                posts.append(each_post)
                unique_set.add(current_post_json_dmp)

    # Private helper method to sort post list
    def __sort_posts(self, post_list, sort_by, ordering):
        is_reverse = False  # Default Ascending
        if ordering == "desc":
            is_reverse = True
        sorted_post_list = sorted(post_list, key=lambda post: post[sort_by], reverse=is_reverse)
        return sorted_post_list
