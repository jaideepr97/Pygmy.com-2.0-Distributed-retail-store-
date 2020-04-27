docker rm order-a &&
docker run --network=myNetwork -p 34601:34601 --name order-a order-a &