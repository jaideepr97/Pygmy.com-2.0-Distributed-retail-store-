import sys
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import random
import string
import threading
from marshmallow import Schema, fields
import json
import time
import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = str(sys.argv[2])

db = SQLAlchemy(app)  # defining the sqlite db
log_file = str(sys.argv[3])

# defining various urls

catalog_url = None
isLocal = False
with open('config.json') as f:
    host_details = json.load(f)
    isLocal = True if host_details['location'] == 0 else False

catalog_url = 'http://0.0.0.0' if isLocal else 'http://elnux1.cs.umass.edu'
primary_path = 'primary_details.json' if isLocal else 'order/order_A/primary_details.json'


log_lock = threading.Lock()  # lock for calculating performance metrics

primary_details = None
with open(primary_path) as f:
  primary_details = json.load(f)


class PurchaseRequest(db.Model):
    """
    This class defines the model for our Orders database, which stores the
    details of all the orders that are successful.
    """
    id = db.Column(db.String(16), primary_key=True)  # unique id
    book_name = db.Column(db.String(16))  # name of the item
    item_number = db.Column(db.Integer, nullable=False)  # item number
    total_price = db.Column(db.Float, nullable=False)  # total price of the order
    remaining_stock = db.Column(db.Integer)  # remaining stock
    date_created = db.Column(db.DateTime, default=datetime.utcnow())  # date and time of the order


class PurchaseRequestSchema(Schema):
    """
    This class defines the schema for our order database,
    which is used to create a JSON dump from an sqlite query object
    """
    id = fields.Str(dump_only=True)
    book_name = fields.Str(dump_only=True)
    item_number = fields.Int()
    total_price = fields.Float()
    remaining_stock = fields.Int()
    date_created = fields.DateTime()


def shutdown_server():
    """
    This function is used to shut down the server
    :return: response
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    """
    This function receives the heartbeat from front end and sends a response
    :return: response
    """
    return '', 200


@app.route('/buy/<int:args>')
def buy(args):
    """
    This function facilitates a buy request
    :param args: item id
    :return: result
    """
    # note the request start time
    request_start = datetime.now()
    request_id = request.values['request_id']

    if primary_details is not None:
        # form the query url and get the result
        port = str(primary_details[str(args)])
        query_url = catalog_url + ':' + port + '/query_by_item/' + str(args)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        request_success = False
        while not request_success:
            try:
                query_result = requests.get(url=query_url, data={'request_id': request_id})
                query_data = query_result.json()

                # if the item is in stock
                if query_data is not None and query_data['result']['quantity'] > 0:

                    # form the query url and get the result
                    update_url = catalog_url + ':' + port + '/update/' + str(args)
                    update_result = requests.get(url=update_url, data={'request_id': request_id})
                    update_data = update_result.json()

                    # if the item is in stock
                    if update_data['result'] == 0:
                        request_success = True
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
                        file = open(log_file, "a+")
                        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
                        file.close()
                        log_lock.release()

                        # return the result
                        return {'result': 'Buy Successful', 'data': result, 'catalog_host/ip':update_data['catalog_host/ip'],
                                  'order_host/ip': hostname+'/'+ip}

                    # if the item is not in stock
                    else:
                        # return failure
                        return {'result': 'Buy Failed!',
                                'data': {'book_name': query_data['result']['name'], 'item_number': args, 'remaining_stock': 0},
                                'catalog_host/ip': update_data['catalog_host/ip'],
                                'order_host/ip': hostname + '/' + ip
                                }
                # if the item is not in stock
                else:
                    # return failure
                    return {'result': 'Buy Failed!',
                            'data': {'book_name': query_data['result']['name'], 'item_number': args, 'remaining_stock': 0},
                            'catalog_host/ip': update_data['catalog_host/ip'],
                            'order_host/ip': hostname + '/' + ip
                            }

            except Exception:
                time.sleep(3)


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """
    This function is used to shut down the server
    :return: response
    """
    shutdown_server()
    return 'Order Server shutting down...'


if __name__ == '__main__':
    '''
    Starting point of the application
    '''
    app.run(host='0.0.0.0', port=sys.argv[1])
