#!/bin/bash
source venv/bin/activate &&
pip3 install -r requirements.txt --user &&
python3 set_config.py 1 &&
python3 order/order_A/order.py 34601 'sqlite:///orders_A.db' 'order/order_A/order_A_log.txt'

