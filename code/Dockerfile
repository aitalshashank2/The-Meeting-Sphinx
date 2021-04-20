FROM python:3.9.4-alpine

ENV PYTHONUNBUFFERED 1  

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev jpeg-dev zlib-dev libjpeg cargo

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
