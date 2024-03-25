FROM python:3.12.2-alpine3.19

WORKDIR /usr/src/app

RUN apk update

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
