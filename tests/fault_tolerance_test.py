import uuid
import datetime
import requests
import random
import time
import threading
import json


operations = ['lookup/1', 'buy/1', 'lookup/1', 'lookup/2', 'buy/2', 'lookup/2', 'buy/3', 'buy/4', 'buy/5',
              'buy/6', 'lookup/3', 'lookup/4', 'lookup/5', 'lookup/6']
frontend_url = 'http://elnux3.cs.umass.edu:34600/'
catalog_a_url = 'http://elnux1.cs.umass.edu:34602/shutdown'
catalog_b_url = 'http://elnux1.cs.umass.edu:34612/shutdown'
order_a_url = 'http://elnux2.cs.umass.edu:34601/shutdown'
order_b_url = 'http://elnux2.cs.umass.edu:34611/shutdown'
# frontend_url = 'http://0.0.0.0:34600/'
# catalog_a_url = 'http://0.0.0.0:34602/shutdown'
# catalog_b_url = 'http://0.0.0.0:34612/shutdown'
# order_a_url = 'http://0.0.0.0:34601/shutdown'
# order_b_url = 'http://0.0.0.0:34611/shutdown'
# local_url = 'http://0.0.0.0:34600'


def process_killer():

    for _ in range(6):
        request_result = requests.get(url=catalog_a_url)
        print(request_result.text)
        time.sleep(10)
        request_result = requests.get(url=catalog_b_url)
        print(request_result.text)
        time.sleep(4)
        request_result = requests.get(url=order_a_url)
        print(request_result.text)
        time.sleep(4)
        request_result = requests.get(url=order_b_url)
        print(request_result.text)
        time.sleep(2)
    pass


def client():

    total_request_time = 0
    request_counter = 0
    file = open("fault_tolerance_test_output.txt", "w")
    file.close()
    file = open("fault_tolerance_test_metrics.txt", "w")
    file.close()
    for i, operation in enumerate(operations):
        request_id = uuid.uuid1()
        request_start = datetime.datetime.now()
        query_url = frontend_url + operation
        # query_url = local_url + '/' + str(operation) + '/' + str(topic)
        print('Request: ' + operation)
        request_result = requests.get(url=query_url, data={'request_id': request_id})
        file = open("fault_tolerance_test_output.txt", "a+")
        file.write(operation+'\n')
        data = json.loads(request_result.text)
        file.write(json.dumps(data, indent=2))
        file.write('\n')
        file.close()
        request_end = datetime.datetime.now()
        request_time = request_end - request_start
        total_request_time = total_request_time + (request_time.microseconds / 1000)
        request_counter = request_counter + 1
        file = open("fault_tolerance_test_metrics.txt", "a+")
        file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
        file.close()
        print('Sent request ' + str(i + 1))
        time.sleep(10)

    file = open("fault_tolerance_test_metrics.txt", "a+")
    file.write("Average request processing time: {}\n".format(total_request_time / request_counter))
    file.write("End to end request processing time: {}\n".format(total_request_time))
    file.close()


if __name__ == '__main__':

    t1 = threading.Thread(target=client)
    t2 = threading.Thread(target=process_killer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done running fault tolerance test")

