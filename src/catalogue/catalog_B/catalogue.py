import sys
import time
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import threading
import datetime
from flask import request
from flask import jsonify
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = str(sys.argv[2])

db = SQLAlchemy(app)    # defining the sqlite database
write_lock = threading.Lock()  # lock for updating the database
log_lock = threading.Lock()  # lock for calculating performance metrics

replica_host = None
with open('config.json') as f:
    host_details = json.load(f)
    replica_host = 'http://0.0.0.0' if host_details['location'] == 0 else 'http://elnux1.cs.umass.edu'

current_port = str(sys.argv[1])
replica_port = str(sys.argv[3])
log_file = str(sys.argv[4])

'''
This class defines the model for out catalog database, which stores the details
about all the stock in Pygmy.com
'''


class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # item number
    name = db.Column(db.String(200), nullable=False)  # name of the book
    quantity = db.Column(db.Integer, nullable=False)  # total available stock
    cost = db.Column(db.Float, nullable=False)  # cost per unit
    topic = db.Column(db.String(100), nullable=False)  # topic of the item


'''
This class defines the schema for our catalog database,
which is used to create a JSON dump from an sqlite query object
'''


class CatalogSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    quantity = fields.Int()
    cost = fields.Float()
    topic = fields.Str()


'''
This function is used to shut down the server
'''


def shutdown_server():

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


'''
This function is used to query by topic
'''


@app.route('/query_by_subject/<args>', methods=["GET"])
def query_by_subject(args):

    # note the request start time
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # query the catalog db
    catalogs_schema = CatalogSchema(many=True)
    catalogs = Catalog.query.with_entities(Catalog.name, Catalog.id).filter_by(topic=args.lower()).all()

    # dump the result in a JSON
    result = catalogs_schema.dump(catalogs)

    # note the request end time and calculate the difference
    request_end = datetime.datetime.now()
    request_time = request_end - request_start

    # acquire a lock on the file and write the time taken
    log_lock.acquire()
    file = open(log_file, "a+")
    file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
    file.close()
    log_lock.release()

    # return the result
    return {'results': result}


'''
This function is used to query by item number
'''


@app.route('/query_by_item/<int:args>', methods=["GET"])
def query_by_item(args):

    # note the request start time
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # query the catalog db
    catalog_schema = CatalogSchema()
    catalog = Catalog.query.with_entities(Catalog.name, Catalog.quantity, Catalog.cost).filter_by(id=args).first()

    # dump the result in a JSON
    result = catalog_schema.dump(catalog)
    replica = 'catalog_a' if current_port == '34602' else 'catalog_b'
    result['replica'] = replica

    # note the request end time and calculate the difference
    request_end = datetime.datetime.now()
    request_time = request_end - request_start

    # acquire a lock on the file and write the time taken
    log_lock.acquire()
    file = open(log_file, "a+")
    file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
    file.close()
    log_lock.release()

    # return the result
    return {'result': result}


'''
This function is used to update the data of the item 
corresponding to the item number
'''


@app.route('/update/<int:args>', methods=["GET"])
def update(args):

    # note the request start time
    # request_start = datetime.datetime.now()
    # request_id = request.values['request_id']

    # acquire a lock on the catalog db to update the item
    write_lock.acquire()

    # query the catalog db
    catalog = db.session.query(Catalog).filter_by(id=args).with_for_update().first()

    # check if the quantity is gt 0
    if catalog is not None and catalog.quantity > 0:

        # update the db, commit and release lock
        catalog.quantity -= 1
        db.session.commit()

        # update the replica
        try:
            replica_url = replica_host + ':' + replica_port + '/update_replica/' + str(args)
            replica_update_request = requests.get(url=replica_url, data={'quantity': catalog.quantity})
        except Exception:
            print('Exception occurred while writing to replica')
        else:
            if replica_update_request.json()['result'] == -1:
                print('Exception occurred while writing to replica')
        finally:
            write_lock.release()

            # note request end time and calculate difference
            # request_end = datetime.datetime.now()
            # request_time = request_end - request_start

            # acquire a lock on the file and write the time taken
            # log_lock.acquire()
            # file = open(log_file, "a+")
            # file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
            # file.close()
            # log_lock.release()

            # return success with remaining stock
            return {'result': 0, 'remaining_stock': catalog.quantity}

    # quantity == 0, return failure
    else:

        # end db session and release lock
        db.session.commit()
        write_lock.release()

        # note request end time and calculate difference
        request_end = datetime.datetime.now()
        request_time = request_end - request_start

        # acquire a lock on the file and write the time taken
        log_lock.acquire()
        file = open(log_file, "a+")
        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
        file.close()
        log_lock.release()

        # return failure
        return {'result': -1}


@app.route('/update_replica/<int:args>', methods=['GET'])
def update_replica(args):

    try:
        catalog = db.session.query(Catalog).filter_by(id=args).with_for_update().first()
        catalog.quantity = request.values['quantity']
        db.session.commit()
        print('Replica updated for id: %d' % args)
    except Exception:
        return {'result': -1}
    else:
        return {'result': 0}


'''
This function is used to shut down the server
'''


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Catalog Server shutting down...'


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200


@app.route('/resync_catalog_db', methods=['GET'])
def resync_catalog_db():
    updated_db = requests.get(url=replica_host + ':' + replica_port + '/request_restore_catalog_db')
    updated_db_data = updated_db.json()['quantities']
    write_lock.acquire()
    catalog = db.session.query(Catalog).all()
    for c in catalog:
        c.quantity = updated_db_data[str(c.id)]
    db.session.commit()
    write_lock.release()
    return '', 200


@app.route('/request_restore_catalog_db', methods=['GET'])
def request_restore_catalog_db():
    restore_quantities = {}
    write_lock.acquire()
    catalog = db.session.query(Catalog).all()
    for c in catalog:
        restore_quantities[c.id] = c.quantity
    write_lock.release()
    return jsonify({'quantities': restore_quantities})

'''
Starting point of the application
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
