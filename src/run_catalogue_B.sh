source venv/bin/activate &&
pip install -r requirements.txt &&
python3 catalogue/catalog_B/catalogue.py 34612 'sqlite:///catalog_B.db' 34602 'catalogue/catalog_B/catalog_B_log.txt'

