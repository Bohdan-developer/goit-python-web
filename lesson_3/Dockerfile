FROM python:3.9.6-slim-bullseye

WORKDIR app

RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY main.py main.py
COPY AddressBook.py AddressBook.py

CMD python main.py
