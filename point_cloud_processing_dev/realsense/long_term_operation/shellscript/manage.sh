#!/bin/bash

set -x

source $(pipenv --venv)/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/pi/.virtualenvs/long_term_operation-xGPKtD-z/lib//python3.7/site-packages/pyrealsense2
#python check_weather_client.py 2>> log.txt
python measure_pc_to_csv.py
python scp_client.py
