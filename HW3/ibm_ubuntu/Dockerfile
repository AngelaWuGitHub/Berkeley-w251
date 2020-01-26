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
    apt-get install -y s3fs && \
	echo "a31221049778484a9608829383537f8b:779a9480e4a39af62f464e4eeb3c2edc8eb48bc71bf9eca2" > $HOME/.cos_creds && \
	chmod 600 $HOME/.cos_creds && \
	mkdir -m 777 /mnt/mybucket && \
    s3fs cos-w251-standard-hw3 /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-south.cloud-object-storage.appdomain.cloud

COPY /ibm_ubuntu/mqtt_subscriber_remote.py mqtt_subscriber_remote.py
