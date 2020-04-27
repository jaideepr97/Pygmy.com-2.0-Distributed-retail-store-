docker rm order-b &&
docker run --network=myNetwork -p 34611:34611 --name order-b jaideepr97/cs677-pygmy.com:order-b &