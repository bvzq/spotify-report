FROM python:3
RUN mkdir /service

WORKDIR /service
COPY ./ /service/

RUN pip install -r requirements.txt

RUN python3 createDB.py
RUN python3 populateStockifyDB.py