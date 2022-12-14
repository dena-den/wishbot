FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

WORKDIR /api
EXPOSE 8000

COPY /requirements.txt ./requirements.txt
RUN pip install -r /api/requirements.txt

COPY /app ./app
COPY /main.py ./main.py

RUN adduser --disabled-password --no-create-home app

ENV PYTHONPATH=/:/api

USER app