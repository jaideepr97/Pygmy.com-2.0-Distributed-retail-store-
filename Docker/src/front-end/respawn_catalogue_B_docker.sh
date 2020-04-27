docker rm catalog-b &&
docker run --network=myNetwork -p 34612:34612 --name catalog-b jaideepr97/cs677-pygmy.com:catalog-b &