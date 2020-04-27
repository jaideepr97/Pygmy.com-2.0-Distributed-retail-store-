docker rm catalog-a &&
docker run --network=myNetwork -p 34602:34602 --name catalog-a jaideepr97/cs677-pygmy.com:catalog-a &