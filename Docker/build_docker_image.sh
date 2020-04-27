cd src &&
python3 set_config.py 0 &&
cd catalogue/catalog_A &&
sudo docker image build -t jaideepr97/cs677-pygmy.com:catalog-a . &&
cd ../catalog_B &&
sudo docker image build -t jaideepr97/cs677-pygmy.com:catalog-b . &&
cd ../../front-end &&
sudo docker image build -t jaideepr97/cs677-pygmy.com:front-end . &&
cd ../order/order_A &&
sudo docker image build -t jaideepr97/cs677-pygmy.com:order-a . &&
cd ../order_B &&
sudo docker image build -t jaideepr97/cs677-pygmy.com:order-b . &&
cd ../../../