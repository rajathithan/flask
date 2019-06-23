from orders import get_model
from flask_restful import Resource

builtin_list = list


class api_orderslist(Resource):
    def get(self):
        return get_model().readall()


class api_ordersno(Resource):
    def get(self, orderno):
        return get_model().find_by_orderno(orderno)


