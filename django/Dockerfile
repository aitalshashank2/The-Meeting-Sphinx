FROM python:3.9.4-alpine

ENV PYTHONUNBUFFERED 1 

RUN addgroup --system django && adduser --system -G django django

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev jpeg-dev zlib-dev libjpeg cargo

RUN pip install --upgrade pip \ 
    && pip install --upgrade setuptools \ 
    && pip install --upgrade pipenv \ 
    && pip install --upgrade supervisor

WORKDIR /

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN mkdir -p /static \
    && chown -R django:django /static \
    && chmod -R o+r /static

RUN mkdir -p /media \
    && chown -R django:django /media \
    && chmod -R o+r /media

RUN mkdir -p /server_logs/supervisord/ \ 
    && mkdir -p /server_logs/gunicorn/ \ 
    && mkdir -p /server_logs/daphne/

VOLUME /static /media /server_logs

COPY ./supervisord.conf ./supervisord.conf

COPY ./gunicorn.conf.py ./gunicorn.conf.py

RUN chown django:django ./supervisord.conf \ 
    && chown django:django ./gunicorn.conf.py

COPY ./code ./code

WORKDIR /code
