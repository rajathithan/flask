import orders
import config
from flask_restful import Api
from orders.orders_api import api_orderslist, api_ordersno
from orders.giftcards_api import api_gclist, api_gcno


app = orders.create_app(config)

api = Api(app)

# order APIs
api.add_resource(api_orderslist, '/api/orders')
api.add_resource(api_ordersno, '/api/orders/<string:orderno>')

# giftcard APIs
api.add_resource(api_gclist, '/api/giftcards')
api.add_resource(api_gcno, '/api/giftcards/<string:gcno>')

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
