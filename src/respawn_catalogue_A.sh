#!/bin/sh
user="$(cat username.txt)"
ssh ${user}@elnux1.cs.umass.edu "sh -c 'cd cs677/lab-3-lab-3-rao-gupta/src; nohup chmod +x run_catalogue_A.sh; nohup ./run_catalogue_A.sh > /dev/null 2>&1 &'"
#echo "respawn_catalogue_A"