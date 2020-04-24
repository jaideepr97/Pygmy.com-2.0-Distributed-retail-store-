python3 fault_tolerance_test.py; cd .. &&
sleep .5
curl http://elnux1.cs.umass.edu:34602/shutdown
#curl http://0.0.0.0:34602/shutdown
sleep .5
curl http://elnux2.cs.umass.edu:34601/shutdown
#curl http://0.0.0.0:34601/shutdown
sleep .5
curl http://elnux1.cs.umass.edu:34612/shutdown
#curl http://0.0.0.0:34612/shutdown
sleep .5
curl http://elnux2.cs.umass.edu:34611/shutdown
#curl http://0.0.0.0:34611/shutdown
sleep .5
curl http://elnux3.cs.umass.edu:34600/shutdown
#curl http://0.0.0.0:34600/shutdown


