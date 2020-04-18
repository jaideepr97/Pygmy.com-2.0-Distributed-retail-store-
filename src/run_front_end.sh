#!/bin/sh
source venv/bin/activate &&
pip install -r requirements.txt --user &&
python3 front-end/front-end.py

