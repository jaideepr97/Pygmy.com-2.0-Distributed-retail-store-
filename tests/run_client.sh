python3 test4.py; cd ..;
sleep .5
curl http://elnux1.cs.umass.edu:34602/shutdown
sleep .5
curl http://elnux2.cs.umass.edu:34601/shutdown
sleep .5
curl http://elnux1.cs.umass.edu:34612/shutdown
sleep .5
curl http://elnux2.cs.umass.edu:34611/shutdown
sleep .5
curl http://elnux3.cs.umass.edu:34600/shutdown
