#!/bin/bash
user="$(cat username.txt)"
remote_path="$(cat remote_path.txt)"
ssh ${user}@elnux2.cs.umass.edu "sh -c 'cd ${remote_path}/lab-3-lab-3-rao-gupta/src; nohup chmod +x run_order_A.sh; nohup ./run_order_A.sh > /dev/null 2>&1 &'"
#./run_order_A.sh