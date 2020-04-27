cd src &&
python3 set_config.py 0 &&
cd catalogue/catalog_A &&
sudo docker image build -t catalog-a . &&
cd ../catalog_B &&
sudo docker image build -t catalog-b . &&
cd ../../front-end &&
sudo docker image build -t front-end . &&
cd ../order/order_A &&
sudo docker image build -t order-a . &&
cd ../order_B &&
sudo docker image build -t order-b . &&
cd ../../../