from flask import Flask
import requests
import datetime
from flask import request
from IPython import embed
import threading

app = Flask(__name__)

'''
Defining various urls
'''
edLab_url = 'http://elnux1.cs.umass.edu:34602'
edLab_order_url = 'http://elnux2.cs.umass.edu:34601'
local_url = 'http://0.0.0.0:34602'
local_order_url = 'http://0.0.0.0:34601'

log_lock = threading.Lock()  # lock for calculating performance metrics


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
def search(args):

    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # form the query url and get the result
    query_url = edLab_url + '/query_by_subject/' + str(args)
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


'''
This function is used to query by item number
'''


@app.route('/lookup/<args>', methods=["GET"])
def lookup(args):

    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # form the query url and get the result
    query_url = edLab_url + '/query_by_item/' + str(args)
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


'''
This function is used to send a buy request
'''


@app.route('/buy/<args>', methods=["GET"])
def buy(args):

    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']

    # form the query url and get the result
    query_url = edLab_order_url + '/buy/' + str(args)
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
