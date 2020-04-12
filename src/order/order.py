from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import random
import string
import threading
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)  # defining the sqlite db

# defining various urls
edLab_url = 'http://elnux1.cs.umass.edu:34602'
local_url = 'http://0.0.0.0:34602'

log_lock = threading.Lock()  # lock for calculating performance metrics


'''
This class defines the model for our Orders database, which stores the
details of all the orders that are successful.
'''


class PurchaseRequest(db.Model):
    id = db.Column(db.String(16), primary_key=True)  # unique id
    book_name = db.Column(db.String(16))  # name of the item
    item_number = db.Column(db.Integer, nullable=False)  # item number
    total_price = db.Column(db.Float, nullable=False)  # total price of the order
    remaining_stock = db.Column(db.Integer)  # remaining stock
    date_created = db.Column(db.DateTime, default=datetime.utcnow())  # date and time of the order


'''
This class defines the schema for our order database,
which is used to create a JSON dump from an sqlite query object
'''


class PurchaseRequestSchema(Schema):
    id = fields.Str(dump_only=True)
    book_name = fields.Str(dump_only=True)
    item_number = fields.Int()
    total_price = fields.Float()
    remaining_stock = fields.Int()
    date_created = fields.DateTime()


'''
This function is used to shut down the server
'''


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


'''
This function facilitates a buy request
'''


@app.route('/buy/<int:args>')
def buy(args):

    # note the request start time
    request_start = datetime.now()
    request_id = request.values['request_id']

    # form the query url and get the result
    query_url = edLab_url + '/query_by_item/' + str(args)
    query_result = requests.get(url=query_url, data={'request_id': request_id})
    query_data = query_result.json()

    # if the item is in stock
    if query_data is not None and query_data['result']['quantity'] > 0:

        # form the query url and get the result
        update_url = edLab_url + '/update/' + str(args)
        update_result = requests.get(url=update_url, data={'request_id': request_id})
        update_data = update_result.json()

        # if the item is in stock
        if update_data['result'] == 0:

            # create a unique order id
            _id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

            # create an order db object and add to orders db
            purchase_request = PurchaseRequest(id=_id, book_name=query_data['result']['name'], item_number=args,
                                               total_price=query_data['result']['cost'],
                                               remaining_stock=update_data['remaining_stock'])
            db.session.add(purchase_request)
            db.session.commit()

            # get the newly created order details
            order_details = PurchaseRequest.query.filter_by(id=_id).first()
            order_schema = PurchaseRequestSchema()
            result = order_schema.dump(order_details)

            # note the request end time and calculate the difference
            request_end = datetime.now()
            request_time = request_end - request_start

            # acquire a lock on the file and write the time
            log_lock.acquire()
            file = open("order_server.txt", "a+")
            file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
            file.close()
            log_lock.release()

            # return the result
            return {'Buy Successful': result}

        # if the item is not in stock
        else:
            # return failure
            return {'Buy Failed!': {'book_name': query_data['result']['name'], 'item_number': args, 'remaining_stock': 0}}

    # if the item is not in stock
    else:
        # return failure
        return {'Buy Failed!': {'book_name': query_data['result']['name'], 'item_number': args, 'remaining_stock': 0}}


'''
This function is used to shut down the server
'''


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Order Server shutting down...'

'''
Starting point of the application
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34601, debug=True)
