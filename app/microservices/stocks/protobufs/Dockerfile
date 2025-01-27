FROM python:3

RUN mkdir /service
<<<<<<< HEAD

WORKDIR /service
COPY ./ /service/

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "./stocks.py"]
=======
COPY ./ /service/
WORKDIR /service
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "stocks.py"]
>>>>>>> 315d7a26507b79492d39115255acbbe69881a292
