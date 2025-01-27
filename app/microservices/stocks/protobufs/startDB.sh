#!/bin/sh
sudo service mysql start
python3 createDB.py
python3 populateStockifyDB.py
