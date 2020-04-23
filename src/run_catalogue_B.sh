#!/bin/bash
source venv/bin/activate &&
pip3 install -r requirements.txt --user &&
python3 set_config.py 1 &&
python3 catalogue/catalog_B/catalogue.py 34612 'sqlite:///catalog_B.db' 34602 'catalogue/catalog_B/catalog_B_log.txt'

