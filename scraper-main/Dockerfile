# FROM python:3.8-slim
FROM debian:latest
MAINTAINER Jasper van den Hoven - jjvdh@tutanota.com
WORKDIR /app

COPY CodeBase/ /app/CodeBase/
COPY CodeBase/google_maps_modules/* /app/CodeBase/google_maps_modules/
COPY Files/requirements.txt requirements.txt
COPY search_terms_mp.txt /app/search_terms_mp.txt
COPY search_terms_gm.txt /app/search_terms_gm.txt

RUN apt update && apt upgrade -y
RUN apt install -y python3-pip python3-dev python3-wheel libxml2-dev libxslt-dev g++ gcc libxslt-dev zlib1g-dev libjpeg-dev libpng-dev \
    curl unzip xvfb libxi6 libgconf-2-4
RUN apt install -y openjdk-11-jdk chromium chromium-driver
RUN mkdir Output && mkdir Output/Instagram
RUN pip3 install -r requirements.txt
RUN apt autoremove -y

WORKDIR /app/CodeBase

CMD ["python3", "main.py"]