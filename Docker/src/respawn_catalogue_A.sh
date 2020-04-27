#!/bin/bash
user="$(cat username.txt)"
remote_path="$(cat remote_path.txt)"
ssh ${user}@elnux1.cs.umass.edu "sh -c 'cd ${remote_path}/lab-3-lab-3-rao-gupta/src; nohup chmod +x run_catalogue_A.sh; nohup ./run_catalogue_A.sh > /dev/null 2>&1 &'"
#./run_catalogue_A.sh