#!/bin/bash
source venv/bin/activate &&
pip install -r requirements.txt --user &&
python set_config.py 0 &&
python catalogue/catalog_B/catalogue.py 34612 'sqlite:///catalog_B.db' 34602 'catalogue/catalog_B/catalog_B_log.txt' 'catalogue/catalog_B/catalog_B_output.txt'

