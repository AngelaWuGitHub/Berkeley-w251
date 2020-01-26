FROM alpine:3.11.3

MAINTAINER Weixin (Angela) Wu

LABEL version = "1.0"

WORKDIR /

RUN apk update && apk add mosquitto-clients python3
RUN pip3 install paho-mqtt

COPY /jetson_mqtt_forwarder/mqtt_subscriber_local.py mqtt_subscriber_local.py