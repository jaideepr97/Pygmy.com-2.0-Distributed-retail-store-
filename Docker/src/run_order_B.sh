#!/bin/bash
source venv/bin/activate &&
pip install -r requirements.txt --user &&
python set_config.py 0 &&
python order/order_B/order.py 34611 'sqlite:///orders_B.db' 'order/order_B/order_B_log.txt'

