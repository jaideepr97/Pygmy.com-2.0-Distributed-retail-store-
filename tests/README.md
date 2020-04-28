# CS 677 - LAB 3 - Experiments

## Experiment 1:
 This experiment is used to test the caching mechanism. Sequential requests with the same arguments are sent and the response time is calculated. Then, a 'buy' request is sent to invalidate the cache. 
 The time taken for subsequent requests is measured.
 
 ## Experiment 2:
 This experiment is used to test consistency. 100 sequential requests are sent to see if consistency is maintained.
 
 ## Experiment 3:
 This experiment is also used to test consistency. The requests are same as experiment 2, but this time
 two clients send the requests concurrently.
 
 ## Experiment 4:
 This experiment is used to test fault tolerance. Sequential requests are sent
 using one thread, while parallelly, another thread randomly kills a server.
 
 ## Results
 
 The results can be seen in the \<test\>_output.txt file created in this dir. The metrics can be found in the \<test\>_metrics.txt file created 
 in this dir.

