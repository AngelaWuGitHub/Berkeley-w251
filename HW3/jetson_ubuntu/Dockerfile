FROM ubuntu:18.04

MAINTAINER Weixin (Angela) Wu

LABEL version = "1.0"

WORKDIR /

# Set it via ARG so that it is only available during the build
# Setting it via ENV will result it to persist after the build
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

# Reference: https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
RUN apt-get install -y \
    python3-pip \
    python3-opencv \
    curl \
    mosquitto-clients

RUN pip3 install paho-mqtt

RUN curl -o haarcascade_frontalface_default.xml \
    'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'

COPY /jetson_ubuntu/face_reg.py face_reg.py
