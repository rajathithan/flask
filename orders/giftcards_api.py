from orders import get_model
from flask_restful import Resource

builtin_list = list


class api_gclist(Resource):
    def get(self):
        return get_model().gcreadall()


class api_gcno(Resource):
    def get(self, gcno):
        return get_model().find_by_gcno(gcno)


