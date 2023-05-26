FROM python:3.10-alpine

COPY requirements.txt requirements.txt
RUN apk update && apk upgrade && apk add --no-cache sqlite && \
    pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

EXPOSE 5000
WORKDIR /mdi
