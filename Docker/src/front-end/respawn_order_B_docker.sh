docker rm order-b &&
docker run --network=myNetwork -p 34611:34611 --name order-b order-b &