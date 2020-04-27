cd src &&
python3 set_config.py 0 &&
sleep 1
sudo docker network create myNetwork &&
sleep 1
sudo docker run --network=myNetwork -p 34602:34602 --name catalog-a catalog-a &
echo Started Catalog A
sleep 1
sudo docker run --network=myNetwork -p 34612:34612 --name catalog-b catalog-b &
echo Started Catalog B
sleep 1
sudo docker run --network=myNetwork -p 34601:34601 --name order-a order-a &
echo Started Order A
sleep 1
sudo docker run --network=myNetwork -p 34611:34611 --name order-b order-b &
echo Started Order B
sleep 1
#docker run -v /var/run/docker.sock:/var/run/docker.sock -p 34600:34600 -d front-end
sudo docker run --network=myNetwork -v "/var/run/docker.sock:/var/run/docker.sock:rw" -p 34600:34600 --name front-end front-end &
echo Started Front End
sleep 5
cd ../tests/ && chmod +x run_client.sh && ./run_client.sh
