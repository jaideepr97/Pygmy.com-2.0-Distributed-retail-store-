import uuid
import datetime
import requests
import random
import time
import json

if __name__ == '__main__':

    edLab_url = 'http://elnux3.cs.umass.edu:34600/'
    local_url = 'http://0.0.0.0:34600/'

    url = edLab_url

    total_request_time = 0
    request_counter = 0
    file = open("consistency_test_1_output.txt", "w")
    file.close()
    file = open("consistency_test_1_metrics.txt", "w")
    file.close()
    operations = ['lookup/2', 'buy/2', 'lookup/2', 'lookup/1', 'buy/1', 'lookup/1']
    print('Starting Consistency Test.....')
    for _ in range(10):
        for i, operation in enumerate(operations):
            request_id = uuid.uuid1()
            request_start = datetime.datetime.now()

            query_url = url + operation

            request_result = requests.get(url=query_url, data={'request_id': request_id})
            print(request_result)
            file = open("consistency_test_1_output.txt", "a+")
            file.write(operation+'\n')
            data = json.loads(request_result.text)
            file.write(json.dumps(data, indent=2))
            file.write('\n')
            file.close()
            request_end = datetime.datetime.now()
            request_time = request_end - request_start
            total_request_time = total_request_time + (request_time.microseconds / 1000)
            request_counter = request_counter + 1
            file = open("consistency_test_1_metrics.txt", "a+")
            file.write("{} \t\t\t {}\n".format(request_id, (request_time.microseconds / 1000)))
            file.close()
            print('Sent request ' + str(request_counter))
            time.sleep(1)

    file = open("consistency_test_1_metrics.txt", "a+")
    file.write("Average request processing time: {}\n".format(total_request_time/request_counter))
    file.write("End to end request processing time: {}\n".format(total_request_time))
    file.close()

    print("Done running consistency test")

