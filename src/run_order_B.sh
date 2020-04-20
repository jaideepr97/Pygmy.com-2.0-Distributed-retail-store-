source venv/bin/activate &&
pip install -r requirements.txt &&
python3 set_config.py 1 &&
python3 order/order_B/order.py 34611 'sqlite:///orders_B.db' 'order/order_B/order_B_log.txt'

