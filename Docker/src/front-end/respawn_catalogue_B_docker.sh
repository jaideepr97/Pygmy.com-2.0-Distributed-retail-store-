docker rm catalog-b &&
docker run --network=myNetwork -p 34612:34612 --name catalog-b catalog-b &