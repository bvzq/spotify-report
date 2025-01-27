FROM python:3

RUN mkdir /service
COPY ./ /service/
WORKDIR /service
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["python", "prediction.py"]