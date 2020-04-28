docker pull jaideepr97/cs677-pygmy.com:front-end &&
docker pull jaideepr97/cs677-pygmy.com:catalog-a &&
docker pull jaideepr97/cs677-pygmy.com:catalog-b &&
docker pull jaideepr97/cs677-pygmy.com:order-a &&
docker pull jaideepr97/cs677-pygmy.com:order-b &&
cd src &&
python3 set_config.py 0 &&
sleep 1
docker network create myNetwork &&
sleep 1
docker run --network=myNetwork -p 34602:34602 --name catalog-a jaideepr97/cs677-pygmy.com:catalog-a &
echo Started Catalog A
sleep 1
docker run --network=myNetwork -p 34612:34612 --name catalog-b jaideepr97/cs677-pygmy.com:catalog-b &
echo Started Catalog B
sleep 1
docker run --network=myNetwork -p 34601:34601 --name order-a jaideepr97/cs677-pygmy.com:order-a &
echo Started Order A
sleep 1
docker run --network=myNetwork -p 34611:34611 --name order-b jaideepr97/cs677-pygmy.com:order-b &
echo Started Order B
sleep 1
docker run --network=myNetwork -v "/var/run/docker.sock:/var/run/docker.sock:rw" -p 34600:34600 --name front-end jaideepr97/cs677-pygmy.com:front-end &

echo Started Front End
sleep 5
cd ../tests/ && chmod +x run_client.sh && ./run_client.sh
