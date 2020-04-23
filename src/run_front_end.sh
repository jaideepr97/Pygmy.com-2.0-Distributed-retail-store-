#!/bin/bash
source venv/bin/activate &&
pip3 install -r requirements.txt --user &&
python3 set_config.py 1 &&
python3 front-end/front-end.py 'front-end/front_end_server_log.txt'