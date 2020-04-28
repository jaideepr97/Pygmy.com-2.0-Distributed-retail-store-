#Docker execution:

1. Clone the repository on your local machine
2. Cd into the Docker directory - this contains the run_pygmy_docker.sh script
3. The docker folder also consists of a tests directory, with each directory containing a
different test (testing a different aspect of the system - caching, consistency and fault
tolerance), and a run_client script that calls all these tests.
4. In order to execute the dockerized version of the application simply execute the
run_pygmy_docker.sh script. This will automatically pull all the images for all the
containers from docker-hub onto the local machine , spin them up and execute all the
tests
5. Once all the tests have been executed, corresponding output files as well as server
output files and log files will be generated within each sub-directory for that respective
test