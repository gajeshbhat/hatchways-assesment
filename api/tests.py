import json
import unittest
from flask import Flask
from flask_restful import Api
from api.ping import Ping
from api.blog import Blog
from api.errors import wrong_sortby_input_error, sorting_order_error, no_tag_error
from api.status_codes import SUCCESSFUL_OK, METHOD_NOT_ALLOWED, BAD_REQUEST


class ApiTestPostFetch(unittest.TestCase):
    """This class represents the a Blog API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Ping, '/api/ping')
        self.api.add_resource(Blog, '/api/posts')
        self.client = self.app.test_client

    def test_ping_get(self):
        res = self.client().get('/api/ping')
        self.assertEqual(SUCCESSFUL_OK, res.status_code)
        self.assertIn(json.dumps({"success": True}), json.dumps(json.loads(res.get_data(as_text=True))))

    def test_ping_post(self):
        res = self.client().post('/api/ping')
        self.assertEqual(METHOD_NOT_ALLOWED, res.status_code)
        self.assertIn(json.dumps({"success": False, 'message': 'POST Not Allowed on this Endpoint'}),
                      json.dumps(json.loads(res.get_data(as_text=True))))

    def test_get_post(self):
        res = self.client().get('/api/posts?tags=history&sortBy=likes&direction=desc')
        expected = self.get_test_data('test_data/test_data_param_0.json')
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_post_posts(self):
        res = self.client().post('/api/posts?tags=history&sortBy=likes&direction=desc')
        self.assertEqual(METHOD_NOT_ALLOWED, res.status_code)
        expected = json.dumps({'success': False, 'message': 'POST Not Allowed'})
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_multiple_tags(self):
        res = self.client().get('/api/posts?tags=history,tech&sortBy=likes&direction=desc')
        expected = self.get_test_data('test_data/test_data_param_1.json')
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_no_tags(self):
        res = self.client().get('/api/posts')
        self.assertEqual(BAD_REQUEST, res.status_code)
        expected = no_tag_error
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_just_tag(self):
        res = self.client().get('/api/posts?tags=history')
        expected = self.get_test_data('test_data/test_data_param_2.json')
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_get_post_tag_no_sort_by(self):
        res = self.client().get('/api/posts?tags=health&direction=asc')
        expected = self.get_test_data('test_data/test_data_param_3.json')
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_sort_by_wrong(self):
        res = self.client().get('/api/posts?tags=history&sortBy=name&direction=asc')
        self.assertEqual(BAD_REQUEST, res.status_code)
        expected = wrong_sortby_input_error
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def test_order_by_wrong(self):
        res = self.client().get('/api/posts?tags=history&sortBy=id&direction=bsc')
        self.assertEqual(BAD_REQUEST, res.status_code)
        expected = sorting_order_error
        actual = json.loads(res.get_data(as_text=True))
        self.assertIn(json.dumps(expected), json.dumps(actual))

    def get_test_data(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        return data

    def tearDown(self):
        """teardown all initialized variables."""


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
