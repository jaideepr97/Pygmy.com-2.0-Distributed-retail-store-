from flask import Flask
import requests
import datetime
from flask import request
import threading
from flask_caching import Cache
import time
import subprocess
import sys
import json
from requests.exceptions import Timeout

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

'''
Defining various urls
'''
isLocal = False
catalog_urls = {}
order_urls = {}


with open('config.json') as f:
    host_details = json.load(f)
    isLocal = True if host_details['location'] == 0 else False

if isLocal:
    catalog_urls = {'A': 'http://catalog-a:34602', 'B': 'http://catalog-b:34612'}
    order_urls = {'A': 'http://order-a:34601', 'B': 'http://order-b:34611'}

    # catalog_urls = {'A': 'http://0.0.0.0:34602', 'B': 'http://0.0.0.0:34612'}
    # order_urls = {'A': 'http://0.0.0.0:34601', 'B': 'http://0.0.0.0:34611'}
else:
    catalog_urls = {'A': 'http://elnux1.cs.umass.edu:34602', 'B': 'http://elnux1.cs.umass.edu:34612'}
    order_urls = {'A': 'http://elnux2.cs.umass.edu:34601', 'B': 'http://elnux2.cs.umass.edu:34611'}

log_lock = threading.Lock()  # lock for calculating performance metrics
shared_flag_lock = threading.Lock()  # lock for shared data structure for heartbeat messages (replicas_alive)
shared_buffer_lock = threading.Lock()  # lock for shared data structure for heartbeat messages (buffer)

catalog_replicas_alive = {'A': True, 'B': True}
order_replicas_alive = {'A': True, 'B': True}

if isLocal:
    catalog_respawn_script_commands = {'A': 'chmod +x respawn_catalogue_A_docker.sh; ./respawn_catalogue_A_docker.sh &',
                                       'B': 'chmod +x respawn_catalogue_B_docker.sh; ./respawn_catalogue_B_docker.sh &'}
    order_respawn_script_commands = {'A': 'chmod +x respawn_order_A_docker.sh; ./respawn_order_A_docker.sh &',
                                     'B': 'chmod +x respawn_order_B_docker.sh; ./respawn_order_B_docker.sh &'}

    # catalog_respawn_script_commands = {'A': 'chmod +x respawn_catalogue_A.sh; ./respawn_catalogue_A.sh &',
    #                                    'B': 'chmod +x respawn_catalogue_B.sh; ./respawn_catalogue_B.sh &'}
    # order_respawn_script_commands = {'A': 'chmod +x respawn_order_A.sh; ./respawn_order_A.sh &',
    #                                  'B': 'chmod +x respawn_order_B.sh; ./respawn_order_B.sh &'}
elif not isLocal:
    catalog_respawn_script_commands = {'A': 'chmod +x respawn_catalogue_A.sh && ./respawn_catalogue_A.sh &',
                                       'B': 'chmod +x respawn_catalogue_B.sh && ./respawn_catalogue_B.sh &'}
    order_respawn_script_commands = {'A': 'chmod +x respawn_order_A.sh && ./respawn_order_A.sh &',
                                     'B': 'chmod +x respawn_order_B.sh && ./respawn_order_B.sh &'}

last_order_server = 'A'
last_catalog_server = 'A'
log_file = str(sys.argv[1])

output_file = str(sys.argv[2])
sys.stdout = open(output_file, "a+")
# sys.stdout = open(output_file, "a+")


'''
This function is used to shut down the server
'''


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def respawn_servers():
    while True:
        time.sleep(.5)
        for replica in catalog_replicas_alive:
            if not catalog_replicas_alive[replica]:
                subprocess.call([str(catalog_respawn_script_commands[replica])], shell=True)
                # print("\n====------catalog {} re-spawned-----=====\n".format(replica))
                log_lock.acquire()
                file = open(output_file, "a+")
                file.write("\n====------catalog {} re-spawned-----=====\n".format(replica))

                file.close()
                log_lock.release()

                time.sleep(5)
                resync_response = requests.get(url=catalog_urls[replica] + '/resync_catalog_db')
                while resync_response.status_code != 200:
                    # print("\nRequest to resync failed, retrying for catalog {}...\n".format(replica))

                    log_lock.acquire()
                    file = open(output_file, "a+")
                    file.write("\nRequest to resync failed, retrying for catalog {}...\n".format(replica))

                    file.close()
                    log_lock.release()

                    time.sleep(1)
                    resync_response = requests.get(url=catalog_urls[replica] + '/resync_catalog_db')

                # print(
                #     "\n********** Re-synchronization of catalog DB for replica {} complete *************\n".format(replica))

                log_lock.acquire()
                file = open(output_file, "a+")
                file.write(
                    "\n********** Re-synchronization of catalog DB for replica {} complete *************\n".format(
                        replica))
                file.close()
                log_lock.release()

        for replica in order_replicas_alive:
            if not order_replicas_alive[replica]:
                subprocess.call([str(order_respawn_script_commands[replica])], shell=True)
                # print("\n=====---order {} re-spawned----=====\n".format(replica))
                log_lock.acquire()
                file = open(output_file, "a+")
                file.write("\n=====---order {} re-spawned----=====\n".format(replica))
                file.close()
                log_lock.release()


def heartbeat(destination_server_url):
    while True:
        try:
            time.sleep(1)
            heartbeat_response_url = str(destination_server_url) + '/heartbeat'
            heartbeat_response = requests.get(url=heartbeat_response_url, timeout=3)
            if heartbeat_response.status_code == 200:

                if destination_server_url == catalog_urls['A']:
                    log_lock.acquire()
                    file = open(output_file, "a+")
                    file.write("\ncatalog_A: alive\n")
                    file.close()
                    log_lock.release()
                    shared_flag_lock.acquire()
                    catalog_replicas_alive['A'] = True
                    shared_flag_lock.release()
                elif destination_server_url == catalog_urls['B']:
                    log_lock.acquire()
                    file = open(output_file, "a+")
                    file.write("\ncatalog_B: alive\n")
                    file.close()
                    log_lock.release()
                    shared_flag_lock.acquire()
                    catalog_replicas_alive['B'] = True
                    shared_flag_lock.release()
                elif destination_server_url == order_urls['A']:
                    log_lock.acquire()
                    file = open(output_file, "a+")
                    file.write("\norder_A: alive\n")
                    file.close()
                    log_lock.release()
                    shared_flag_lock.acquire()
                    order_replicas_alive['A'] = True
                    shared_flag_lock.release()
                elif destination_server_url == order_urls['B']:
                    log_lock.acquire()
                    file = open(output_file, "a+")
                    file.write("\norder_B: alive\n")
                    file.close()
                    log_lock.release()
                    shared_flag_lock.acquire()
                    order_replicas_alive['B'] = True
                    shared_flag_lock.release()

        except Exception:
            if destination_server_url == catalog_urls['A']:
                log_lock.acquire()
                file = open(output_file, "a+")
                file.write("\n--------- catalog_A: DEAD-------------\n")
                file.close()
                log_lock.release()
                shared_flag_lock.acquire()
                catalog_replicas_alive['A'] = False
                shared_flag_lock.release()
            elif destination_server_url == catalog_urls['B']:
                log_lock.acquire()
                file = open(output_file, "a+")
                file.write("\n--------- catalog_B: DEAD-------------\n")
                file.close()
                log_lock.release()
                shared_flag_lock.acquire()
                catalog_replicas_alive['B'] = False
                shared_flag_lock.release()
            elif destination_server_url == order_urls['A']:
                log_lock.acquire()
                file = open(output_file, "a+")
                file.write("\n--------- order_A: DEAD-------------\n")
                file.close()
                log_lock.release()
                shared_flag_lock.acquire()
                order_replicas_alive['A'] = False
                shared_flag_lock.release()
            elif destination_server_url == order_urls['B']:
                log_lock.acquire()
                file = open(output_file, "a+")
                file.write("\n--------- order_B: DEAD-------------\n")
                file.close()
                log_lock.release()
                shared_flag_lock.acquire()
                order_replicas_alive['B'] = False
                shared_flag_lock.release()


'''
This function is used to search by topic
'''


@app.route('/search/<args>', methods=["GET"])
@cache.memoize()
def search(args):
    global last_catalog_server
    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']
    request_success = False

    while not request_success:
        # form the query url using load balancing (round robin)
        shared_flag_lock.acquire()
        if catalog_replicas_alive[last_catalog_server]:
            query_url = catalog_urls[last_catalog_server] + '/query_by_subject/' + str(args)
            # print("Search request being handled by catalog {}\n".format(last_catalog_server))

            log_lock.acquire()
            file = open(output_file, "a+")
            file.write("Search request being handled by catalog {}\n".format(last_catalog_server))
            file.close()
            log_lock.release()
        else:
            # global last_catalog_server

            last_catalog_server = 'A' if last_catalog_server == 'B' else 'B'
            query_url = catalog_urls[last_catalog_server] + '/query_by_subject/' + str(args)
            # print("Assigned server unavailable, search switching to available server catalog {}\n".format(last_catalog_server))

            log_lock.acquire()
            file = open(output_file, "a+")
            file.write("Assigned server unavailable, search switching to available server catalog {}\n".format(last_catalog_server))
            file.close()
            log_lock.release()

        last_catalog_server = 'A' if last_catalog_server == 'B' else 'B'
        shared_flag_lock.release()

        # get the results
        try:
            query_result = requests.get(url=query_url, data={'request_id': request_id})

            # note the request end time and calculate the difference
            request_end = datetime.datetime.now()
            request_time = request_end - request_start

            # acquire a lock on the file and write the time
            log_lock.acquire()
            file = open(log_file, "a+")
            file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
            file.close()
            log_lock.release()

            # return the results
            request_success = True
            return query_result.json()
        except Exception:
            time.sleep(3)
            pass


'''
This function is used to query by item number
'''


@app.route('/lookup/<args>', methods=["GET"])
@cache.memoize()
def lookup(args):
    global last_catalog_server
    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']
    request_success = False

    while not request_success:
        # form the query url using load balancing (round robin)
        shared_flag_lock.acquire()
        if catalog_replicas_alive[last_catalog_server]:
            query_url = catalog_urls[last_catalog_server] + '/query_by_item/' + str(args)
            # print("Lookup request being handled by catalog {}\n".format(last_catalog_server))

            log_lock.acquire()
            file = open(output_file, "a+")
            file.write("Lookup request being handled by catalog {}\n".format(last_catalog_server))
            file.close()
            log_lock.release()
        else:
            # global last_catalog_server
            last_catalog_server = 'A' if last_catalog_server == 'B' else 'B'
            query_url = catalog_urls[last_catalog_server] + '/query_by_item/' + str(args)
            # print("Assigned server unavailable, lookup switching to available server catalog {}\n".format(
            #     last_catalog_server))

            log_lock.acquire()
            file = open(output_file, "a+")
            file.write("Assigned server unavailable, lookup switching to available server catalog {}\n".format(
                last_catalog_server))
            file.close()
            log_lock.release()
        last_catalog_server = 'A' if last_catalog_server == 'B' else 'B'
        shared_flag_lock.release()

        # get the result
        try:
            query_result = requests.get(url=query_url, data={'request_id': request_id})

            # note the request end time and calculate the difference
            request_end = datetime.datetime.now()
            request_time = request_end - request_start

            # acquire a lock on the file and write the time
            log_lock.acquire()
            file = open(log_file, "a+")
            file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
            file.close()
            log_lock.release()

            # return the results
            request_success = True
            return query_result.json()
        except Exception:
            time.sleep(3)
            pass


'''
This function is used to send a buy request
'''


@app.route('/buy/<args>', methods=["GET"])
def buy(args):
    global last_order_server
    # note the starting time of the request
    request_start = datetime.datetime.now()
    request_id = request.values['request_id']
    request_success = False

    # invalidate cache
    cache.delete_memoized(lookup, args)

    while not request_success:
        # form the query url using load balancing (round robin)
        shared_flag_lock.acquire()
        if order_replicas_alive[last_order_server]:
            query_url = order_urls[last_order_server] + '/buy/' + str(args)
            # print("Buy request being handled by order {}\n".format(last_order_server))
            #
            log_lock.acquire()
            file = open(output_file, "a+")
            file.write("Buy request being handled by order {}\n".format(last_order_server))
            file.close()
            log_lock.release()
        else:
            # global last_order_server
            last_order_server = 'A' if last_order_server == 'B' else 'B'
            query_url = order_urls[last_order_server] + '/buy/' + str(args)
            # print("Assigned server unavailable, buy switching to available server order {}\n".format(
            #     last_order_server))

            log_lock.acquire()
            file = open(output_file, "a+")
            file.write("Assigned server unavailable, buy switching to available server order {}\n".format(
                last_order_server))
            file.close()
            log_lock.release()
        last_order_server = 'A' if last_order_server == 'B' else 'B'
        shared_flag_lock.release()

        # get the result
        try:
            query_result = requests.get(url=query_url, data={'request_id': request_id})
            if query_result.json()['result'] == 'Server Error':
                pass
            else:
                # note the request end time and calculate the difference
                request_end = datetime.datetime.now()
                request_time = request_end - request_start

                # acquire a lock on the file and write the time
                log_lock.acquire()
                file = open(log_file, "a+")
                file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
                file.close()
                log_lock.release()

                # return the results
                request_success = True
                return query_result.json()
        except Exception:
            time.sleep(3)
            pass


'''
This function is used to shut down the server
'''


@app.route('/shutdown', methods=['GET'])
def shutdown():
    sys.stdout.close()
    shutdown_server()
    return 'Front End Server shutting down...'


'''
Starting point of the application
'''
if __name__ == '__main__':

    catalog_A_heartbeat = threading.Thread(target=heartbeat, args=(catalog_urls['A'],))
    catalog_A_heartbeat.start()
    catalog_B_heartbeat = threading.Thread(target=heartbeat, args=(catalog_urls['B'],))
    catalog_B_heartbeat.start()
    order_A_heartbeat = threading.Thread(target=heartbeat, args=(order_urls['A'],))
    order_A_heartbeat.start()
    order_B_heartbeat = threading.Thread(target=heartbeat, args=(order_urls['B'],))
    order_B_heartbeat.start()
    respawn_server_thread = threading.Thread(target=respawn_servers)
    respawn_server_thread.start()
    app.run(host='0.0.0.0', port=34600)
