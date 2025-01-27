FROM python:3

RUN mkdir /service

WORKDIR /service
COPY ./ /service/

RUN pip install -r requirements.txt

EXPOSE 5002
#RUN chmod +x startDB.sh
#RUN ./startDB.sh
CMD ["python", "./account.py"]