FROM alpine:3.11.3

MAINTAINER Weixin (Angela) Wu

LABEL version = "1.0"

WORKDIR /

RUN apk update && apk add mosquitto

RUN rm /etc/mosquitto/mosquitto.conf
COPY /jetson_mqtt_broker/mosquitto.conf /etc/mosquitto/mosquitto.conf
