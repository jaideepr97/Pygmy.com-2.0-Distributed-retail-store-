from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import threading
import datetime
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)    # defining the sqlite database
buy_lock = threading.Lock()  # lock for updating the database
log_lock = threading.Lock()  # lock for calculating performance metrics

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
    file = open("catalog_server.txt", "a+")
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

    # note the request end time and calculate the difference
    request_end = datetime.datetime.now()
    request_time = request_end - request_start

    # acquire a lock on the file and write the time taken
    log_lock.acquire()
    file = open("catalog_server.txt", "a+")
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
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # acquire a lock on the catalog db to update the item
    buy_lock.acquire()

    # query the catalog db
    catalog = db.session.query(Catalog).filter_by(id=args).with_for_update().first()

    # check if the quantity is gt 0
    if catalog is not None and catalog.quantity > 0:

        # update the db, commit and release lock
        catalog.quantity -= 1
        db.session.commit()
        buy_lock.release()

        # note request end time and calculate difference
        request_end = datetime.datetime.now()
        request_time = request_end - request_start

        # acquire a lock on the file and write the time taken
        log_lock.acquire()
        file = open("front_end_server.txt", "a+")
        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
        file.close()
        log_lock.release()

        # return success with remaining stock
        return {'result': 0, 'remaining_stock': catalog.quantity}

    # quantity == 0, return failure
    else:

        # end db session and release lock
        db.session.commit()
        buy_lock.release()

        # note request end time and calculate difference
        request_end = datetime.datetime.now()
        request_time = request_end - request_start

        # acquire a lock on the file and write the time taken
        log_lock.acquire()
        file = open("front_end_server.txt", "a+")
        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
        file.close()
        log_lock.release()

        # return failure
        return {'result': -1}


'''
This function is used to shut down the server
'''


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Catalog Server shutting down...'


'''
Starting point of the application
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34602, debug=True)
