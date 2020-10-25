import json
import unittest

import requests
from flask import Flask
from flask_restful import Api
from api.ping import Ping
from api.blog import Blog


class ApiTestPostFetch(unittest.TestCase):
    """This class represents the a Blog API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Ping, '/api/ping')
        self.api.add_resource(Blog, '/api/posts')
        self.app.testing = True
        self.client = self.app.test_client
        self.test_url_base = "https://api.hatchways.io/assessment/solution/posts"

    def test_ping(self):
        """Test API can ping the endpoint (GET request)"""
        res = self.client().get('/api/ping')
        self.assertEqual(200, res.status_code)
        self.assertIn(json.dumps({"success": True}), json.dumps(json.loads(res.get_data(as_text=True))))

    def test_get_post(self):
        """Test API endpoint posts (GET request)"""
        res = self.client().get('/api/posts?tags=history&sortBy=likes&direction=desc')
        self.assertEqual(200, res.status_code)
        expected = requests.get(self.test_url_base + "?tags=history&sortBy=likes&direction=desc").json()
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_multiple_tags(self):
        """Test API endpoint posts with multiple tags(GET request)"""
        res = self.client().get('/api/posts?tags=history,tech&sortBy=likes&direction=desc')
        self.assertEqual(200, res.status_code)
        expected = requests.get(self.test_url_base + "?tags=history,tech&sortBy=likes&direction=desc").json()
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_no_tags(self):
        """Test API endpoint posts with no tags(GET request)"""
        res = self.client().get('/api/posts')
        self.assertEqual(400, res.status_code)
        expected = requests.get(self.test_url_base).json()
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_just_tag(self):
        """Test API endpoint posts with only tags(GET request)"""
        res = self.client().get('/api/posts?tags=history')
        self.assertEqual(200, res.status_code)
        expected = requests.get(self.test_url_base + "?tags=history").json()
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_tag_no_sort_by(self):
        """Test API endpoint posts with tags and not sort by key(GET request)"""
        res = self.client().get('/api/posts?tags=history&direction=asc')
        self.assertEqual(200, res.status_code)
        expected = requests.get(self.test_url_base + "?tags=history&direction=asc").json()
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def tearDown(self):
        """teardown all initialized variables."""


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
