#!/bin/bash
source venv/bin/activate &&
pip install -r requirements.txt --user &&
python set_config.py 0 &&
python catalogue/catalog_A/catalogue.py 34602 'sqlite:///catalog_A.db' 34612 'catalogue/catalog_A/catalog_A_log.txt' 'catalogue/catalog_A/catalog_A_output.txt'
	
