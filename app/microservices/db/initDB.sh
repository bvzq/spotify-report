#!/bin/sh
apt-get update
apt-get install python3.8
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
service mysql restart
python3 createDB.py
python3 populateStockifyDB.py