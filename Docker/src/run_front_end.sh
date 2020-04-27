#!/bin/bash
source venv/bin/activate &&
pip install -r requirements.txt --user &&
python3 set_config.py 0 &&
python3 front-end/front-end.py 'front-end/front_end_server_log.txt' 'front-end/front_end_server_output.txt'
