#!/bin/bash

user=jrao
remote_path=/nfs/elsrv4/users1/grad/jrao/cs677

ssh ${user}@elnux3.cs.umass.edu "sh -c 'cd cs677/lab-3-lab-3-rao-gupta/src; echo "$user" >> username.txt; nohup chmod +x run_front_end.sh; nohup ./run_front_end.sh > /dev/null 2>&1 &'"
ssh ${user}@elnux1.cs.umass.edu "sh -c 'cd cs677/lab-3-lab-3-rao-gupta/src; nohup chmod +x run_catalogue.sh_A; nohup ./run_catalogue_A.sh; nohup chmod +x run_catalogue_B.sh; nohup ./run_catalogue_B.sh > /dev/null 2>&1 &'"
ssh ${user}@elnux2.cs.umass.edu "sh -c 'cd cs677/lab-3-lab-3-rao-gupta/src; nohup chmod +x run_order_A.sh; nohup ./run_order_A.sh; nohup chmod +x run_order_B.sh; nohup ./run_order_B.sh > /dev/null 2>&1 &'"
#ssh aayushgupta@elnux7.cs.umass.edu "sh -c 'cd cs677/lab-2-rao-gupta/tests; nohup chmod +x run_client.sh; nohup ./run_client.sh > /dev/null 2>&1 &'"
sleep 1
cd tests/ && chmod +x run_client.sh && ./run_client.sh