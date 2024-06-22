# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.12-rc-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "run.py" ]