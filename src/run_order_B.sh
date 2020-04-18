source venv/bin/activate;
pip install -r requirements.txt;
python3 order/order.py 34611 'sqlite:///orders_B.db' 'order/order_B_log.txt'

