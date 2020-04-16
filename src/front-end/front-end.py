from flask import Flask
import requests
import datetime
from flask import request
import threading
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

'''
Defining various urls
'''
# catalog_A_url = 'http://elnux1.cs.umass.edu:34602'
# catalog_B_url = 'http://elnux1.cs.umass.edu:34612'
# order_A_url = 'http://elnux2.cs.umass.edu:34601'
# order_B_url = 'http://elnux2.cs.umass.edu:34611'
catalog_urls = {'A': 'http://0.0.0.0:34602', 'B': 'http://0.0.0.0:34612'}
order_urls = {'A': 'http://0.0.0.0:34601', 'B': 'http://0.0.0.0:34611'}

log_lock = threading.Lock()  # lock for calculating performance metrics
shared_flag_lock = threading.Lock()  # lock for shared data structure for heartbeat messages (replicas_alive)
shared_buffer_lock = threading.Lock() # lock for shared data structure for heartbeat messages (buffer)

replicas_alive = {'A': True, 'B': True}
last_order_server = 'A'
last_catalog_server = 'A'

'''
This function is used to shut down the server
'''


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


'''
This function is used to search by topic
'''


@app.route('/search/<args>', methods=["GET"])
@cache.memoize()
def search(args):

    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # form the query url using load balancing (round robin)
    shared_flag_lock.acquire()
    if replicas_alive[last_catalog_server]:
        query_url = catalog_urls[last_catalog_server] + '/query_by_subject/' + str(args)
    else:
        global last_catalog_server
        last_catalog_server = 'A' if last_catalog_server == 'B' else 'A'
        query_url = catalog_urls[last_catalog_server] + '/query_by_subject/' + str(args)
    last_catalog_server = 'A' if last_catalog_server == 'B' else 'A'
    shared_flag_lock.release()

    # get the results
    try:
        query_result = requests.get(url=query_url, data={'request_id': request_id})

        # note the request end time and calculate the difference
        request_end = datetime.datetime.now()
        request_time = request_end - request_start

        # acquire a lock on the file and write the time
        log_lock.acquire()
        file = open("front_end_server.txt", "a+")
        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
        file.close()
        log_lock.release()

        # return the results
        return query_result.json()
    except Exception:
        # TODO add to shared buffer - request failure (catalogue server down)
        pass


'''
This function is used to query by item number
'''


@app.route('/lookup/<args>', methods=["GET"])
@cache.memoize()
def lookup(args):

    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # form the query url using load balancing (round robin)
    shared_flag_lock.acquire()
    if replicas_alive[last_catalog_server]:
        query_url = catalog_urls[last_catalog_server] + '/query_by_item/' + str(args)
    else:
        global last_catalog_server
        last_catalog_server = 'A' if last_catalog_server == 'B' else 'A'
        query_url = catalog_urls[last_catalog_server] + '/query_by_item/' + str(args)
    last_catalog_server = 'A' if last_catalog_server == 'B' else 'A'
    shared_flag_lock.release()

    # get the result
    try:
        query_result = requests.get(url=query_url, data={'request_id': request_id})

        # note the request end time and calculate the difference
        request_end = datetime.datetime.now()
        request_time = request_end - request_start

        # acquire a lock on the file and write the time
        log_lock.acquire()
        file = open("front_end_server.txt", "a+")
        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
        file.close()
        log_lock.release()

        # return the results
        return query_result.json()
    except Exception:
        # TODO add to shared buffer - request failure (catalogue server down)
        pass


'''
This function is used to send a buy request
'''


@app.route('/buy/<args>', methods=["GET"])
def buy(args):

    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # invalidate cache
    cache.delete_memoized(lookup, args)

    # form the query url using load balancing (round robin)
    shared_flag_lock.acquire()
    if replicas_alive[last_order_server]:
        query_url = order_urls[last_order_server] + '/buy/' + str(args)
    else:
        global last_order_server
        last_order_server = 'A' if last_order_server == 'B' else 'A'
        query_url = order_urls[last_order_server] + '/buy/' + str(args)
    last_order_server = 'A' if last_order_server == 'B' else 'A'
    shared_flag_lock.release()

    # get the result
    try:
        query_result = requests.get(url=query_url, data={'request_id': request_id})
        if query_result.json()['result'] == 'Server Error':
            # TODO add to shared buffer - catalog server down
            pass
        else:
            # note the request end time and calculate the difference
            request_end = datetime.datetime.now()
            request_time = request_end - request_start

            # acquire a lock on the file and write the time
            log_lock.acquire()
            file = open("front_end_server.txt", "a+")
            file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
            file.close()
            log_lock.release()

            # return the results
            return query_result.json()
    except Exception:
        # TODO add to shared buffer - order server down
        pass


'''
This function is used to shut down the server
'''


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Front End Server shutting down...'


'''
Starting point of the application
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34600, debug=True)
