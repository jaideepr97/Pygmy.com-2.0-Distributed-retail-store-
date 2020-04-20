cd src &&
cd catalogue/catalog_A &&
docker image build -t catalog-a . &&
cd ../catalog_B &&
docker image build -t catalog-b . &&
cd ../../front-end &&
docker image build -t front-end . &&
cd ../order/order_A &&
docker image build -t order-a . &&
cd ../order_B &&
docker image build -t order-b . &&
cd ../../../