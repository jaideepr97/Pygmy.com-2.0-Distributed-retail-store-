#!/bin/sh
source venv/bin/activate;
pip install -r requirements.txt;
python3 catalogue/catalogue.py 34602 'sqlite:///catalog_A.db' 34612 'catalogue/catalog_A_log.txt'
	
