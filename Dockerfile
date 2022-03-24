FROM python:3.10.0-buster

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade -r requirements.txt

EXPOSE 8080

COPY . /app
