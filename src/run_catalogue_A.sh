source venv/bin/activate &&
pip3 install -r requirements.txt --user &&
python3 set_config.py 1 &&
python3 catalogue/catalog_A/catalogue.py 34602 'sqlite:///catalog_A.db' 34612 'catalogue/catalog_A/catalog_A_log.txt'
	
