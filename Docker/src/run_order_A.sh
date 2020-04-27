#!/bin/bash
source venv/bin/activate &&
pip install -r requirements.txt --user &&
python set_config.py 0 &&
python order/order_A/order.py 34601 'sqlite:///orders_A.db' 'order/order_A/order_A_log.txt'

