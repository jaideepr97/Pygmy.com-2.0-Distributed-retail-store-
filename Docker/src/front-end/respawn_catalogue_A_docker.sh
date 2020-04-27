docker rm catalog-a &&
docker run --network=myNetwork -p 34602:34602 --name catalog-a catalog-a &