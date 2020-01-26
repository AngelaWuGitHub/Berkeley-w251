FROM ubuntu:18.04

MAINTAINER Weixin (Angela) Wu

LABEL version = "1.0"

WORKDIR /

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y python3-pip mosquitto-clients python3-opencv && \
    pip3 install paho-mqtt

# Mount a Cloud Object storage into your VSI
# Reference: https://github.com/MIDS-scaling-up/2/tree/master/week02/lab2
RUN apt-get install -y automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config && \
    apt-get install -y s3fs
    
COPY /ibm_ubuntu/mqtt_subscriber_remote.py mqtt_subscriber_remote.py
