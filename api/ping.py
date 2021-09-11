from flask_restful import Resource
from .status_codes import SUCCESSFUL_OK, METHOD_NOT_ALLOWED


# Ping Resource
class Ping(Resource):

    def get(self):
        return {"success": True}, SUCCESSFUL_OK

    def post(self):
        return {'success': False, 'message': 'POST Not Allowed on this Endpoint'}, METHOD_NOT_ALLOWED
