FROM python:3.9.6-slim-buster

WORKDIR app

RUN pip install pipenv

COPY . .

RUN pipenv install --system --deploy

CMD python main.py
