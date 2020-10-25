from flask_restful import Resource


# Ping Resource
class Ping(Resource):

    def get(self):
        return {"success": True}, 200

    def post(self):
        return {'success': False, 'message': 'POST Not Allowed on this Endpoint'}, 405
