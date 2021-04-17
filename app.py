import os
import flask
import pymongo


class App:
    def __init__(self):
        if not os.environ.get('PIZZA_ORDERS_MONGODB_HOST') or not os.environ.get('PIZZA_ORDERS_MONGODB_PORT'):
            self._mongodb_host: str = "localhost"
            self._mongodb_port: int = 27018
        else:
            self._mongodb_host: str = os.environ['MONGODB_HOST']
            self._mongodb_port: int = int(os.environ['MONGODB_PORT'])

        if not os.environ.get('FLASK_HOST') or not os.environ.get('FLASK_PORT'):
            self._flask_host: str = "localhost"
            self._flask_port: int = 5555
        else:
            self._flask_host: str = os.environ['FLASK_HOST']
            self._flask_port: int = int(os.environ['FLASK_PORT'])

        self._flask_app: flask.Flask = flask.Flask(__name__)
        self.create_flask_endpoints()
        self._client: pymongo.MongoClient = pymongo.MongoClient(host=self._mongodb_host, port=self._mongodb_port)
        self._db = self._client["orders"]

    def create_flask_endpoints(self):
        @self._flask_app.route('/orders', methods=['GET'])
        def get_orders():
            orders: list = []
            for order in self._db.find():
                orders.append(order)
            #print(orders)
            return flask.jsonify("Hello")

    def run(self):
        print(f"Running app")
        self._flask_app.run(host=self._flask_host, port=self._flask_port)

    def stop(self):
        pass
