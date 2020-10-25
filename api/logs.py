from flask_restful import Resource


# Only for authenticated Developer accounts. TODO : Authentication

class ApiLogs(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        # self.logger - 'logger' from resource_class_kwargs
        return self.logger.name
