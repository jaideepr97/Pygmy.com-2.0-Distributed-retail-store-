cd src &&
python3 set_config.py 0 &&
sleep 1
docker run -p 34602:34602 -d catalog-a &&
echo Started Catalog A
sleep 1
docker run -p 34612:34612 -d catalog-b &&
echo Started Catalog B
sleep 1
docker run -p 34601:34601 -d order-a &&
echo Started Order A
sleep 1
docker run -p 34611:34611 -d order-b &&
echo Started Order B
sleep 1
#docker run -v /var/run/docker.sock:/var/run/docker.sock -p 34600:34600 -d front-end
docker run -p 34600:34600 -d front-end
echo Started Front End