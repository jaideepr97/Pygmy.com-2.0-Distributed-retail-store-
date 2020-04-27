cd caching_test/
python3 caching_test.py &&
sudo docker cp front-end:/src/front_end_server_output.txt front_end_server_output.txt &&
sudo docker cp front-end:/src/front_end_server_log.txt front_end_server_log.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_output.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_log.txt &&

sudo docker cp catalog-a:/src/catalog_A_output.txt catalog_A_output.txt &&
sudo docker cp catalog-a:/src/catalog_A_log.txt catalog_A_log.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_output.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_log.txt &&

sudo docker cp catalog-b:/src/catalog_B_output.txt catalog_B_output.txt &&
sudo docker cp catalog-b:/src/catalog_B_log.txt catalog_B_log.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_output.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_log.txt &&

sudo docker cp order-a:/src/order_A_log.txt order_A_log.txt &&
sudo docker exec order-a rm -rf /src/order_A_log.txt &&

sudo docker cp order-b:/src/order_B_log.txt order_B_log.txt &&
sudo docker exec order-b rm -rf /src/order_B_log.txt &&

sleep 2
cd ../consistency_test_1/
python3 consistency_test_1.py &&

sudo docker cp front-end:/src/front_end_server_output.txt front_end_server_output.txt &&
sudo docker cp front-end:/src/front_end_server_log.txt front_end_server_log.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_output.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_log.txt &&

sudo docker cp catalog-a:/src/catalog_A_output.txt catalog_A_output.txt &&
sudo docker cp catalog-a:/src/catalog_A_log.txt catalog_A_log.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_output.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_log.txt &&

sudo docker cp catalog-b:/src/catalog_B_output.txt catalog_B_output.txt &&
sudo docker cp catalog-b:/src/catalog_B_log.txt catalog_B_log.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_output.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_log.txt &&

sudo docker cp order-a:/src/order_A_log.txt order_A_log.txt &&
sudo docker exec order-a rm -rf /src/order_A_log.txt &&

sudo docker cp order-b:/src/order_B_log.txt order_B_log.txt &&
sudo docker exec order-b rm -rf /src/order_B_log.txt &&

sleep 2
cd ../consistency_test_2/
python3 consistency_test_2.py &&

sudo docker cp front-end:/src/front_end_server_output.txt front_end_server_output.txt &&
sudo docker cp front-end:/src/front_end_server_log.txt front_end_server_log.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_output.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_log.txt &&

sudo docker cp catalog-a:/src/catalog_A_output.txt catalog_A_output.txt &&
sudo docker cp catalog-a:/src/catalog_A_log.txt catalog_A_log.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_output.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_log.txt &&

sudo docker cp catalog-b:/src/catalog_B_output.txt catalog_B_output.txt &&
sudo docker cp catalog-b:/src/catalog_B_log.txt catalog_B_log.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_output.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_log.txt &&

sudo docker cp order-a:/src/order_A_log.txt order_A_log.txt &&
sudo docker exec order-a rm -rf /src/order_A_log.txt &&

sudo docker cp order-b:/src/order_B_log.txt order_B_log.txt &&
sudo docker exec order-b rm -rf /src/order_B_log.txt &&

sleep 10
cd ../fault_tolerance_test/
python3 fault_tolerance_test.py &&

sudo docker cp front-end:/src/front_end_server_output.txt front_end_server_output.txt &&
sudo docker cp front-end:/src/front_end_server_log.txt front_end_server_log.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_output.txt &&
sudo docker exec front-end rm -rf /src/front_end_server_log.txt &&

sudo docker cp catalog-a:/src/catalog_A_output.txt catalog_A_output.txt &&
sudo docker cp catalog-a:/src/catalog_A_log.txt catalog_A_log.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_output.txt &&
sudo docker exec cataog-a rm -rf /src/catalog_A_log.txt &&

sudo docker cp catalog-b:/src/catalog_B_output.txt catalog_B_output.txt &&
sudo docker cp catalog-b:/src/catalog_B_log.txt catalog_B_log.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_output.txt &&
sudo docker exec cataog-b rm -rf /src/catalog_B_log.txt &&

sudo docker cp order-a:/src/order_A_log.txt order_A_log.txt &&
sudo docker exec order-a rm -rf /src/order_A_log.txt &&

sudo docker cp order-b:/src/order_B_log.txt order_B_log.txt &&
sudo docker exec order-b rm -rf /src/order_B_log.txt &&

cd .. &&
sleep 2
curl http://0.0.0.0:34600/shutdown
sleep 2
#curl http://elnux1.cs.umass.edu:34602/shutdown
curl http://0.0.0.0:34602/shutdown
sleep .5
#curl http://elnux2.cs.umass.edu:34601/shutdown
curl http://0.0.0.0:34601/shutdown
sleep .5
#curl http://elnux1.cs.umass.edu:34612/shutdown
curl http://0.0.0.0:34612/shutdown
sleep .5
#curl http://elnux2.cs.umass.edu:34611/shutdown
curl http://0.0.0.0:34611/shutdown
sleep 1
#curl http://elnux3.cs.umass.edu:34600/shutdown
curl http://0.0.0.0:34602/shutdown
sleep 2
curl http://0.0.0.0:34600/shutdown


