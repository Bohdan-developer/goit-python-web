FROM python:3.9-slim-buster

WORKDIR /usr/srs/app

RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY . .


CMD python main.py
