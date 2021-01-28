# FROM python:3.8-slim
FROM debian:latest
MAINTAINER Jasper van den Hoven - jjvdh@tutanota.com
WORKDIR /app

COPY CodeBase/ /app/CodeBase/
COPY Files/requirements.txt requirements.txt
COPY Files/search_terms_ig.txt /app/search_terms_ig.txt

RUN apt update && apt upgrade -y
RUN apt install -y python3-pip python3-dev python3-wheel ffmpeg
RUN mkdir Output && mkdir Output/Instagram
RUN pip3 install -r requirements.txt
RUN apt autoremove -y

WORKDIR /app/CodeBase

CMD ["python3", "main.py"]