## Homework 3 - Internet of Things 101

### Assignment Requirements

* Use OpenCV and write an application that scans the video frames from the connected USB camera for faces
* Cut the faces out of the frame if detected and send it to a local MQTT broker via a binary message
* Receive the message from a local MQTT broker and forward it to a Cloud MQTT broker
* Save the message (converted back to a picture format) in a Cloud Storage

Suggested architecture diagram:  
![Copied from the Assignment](architecture_provided.png)


### Overview of My Implementation

I created five docker containers, three on Jetson TX2 and two on IBM VPC.
1. jetson_ubuntu
    * Built using `./jetson_ubuntu/Dockerfile`
    * Attached to a user-defined network called `hw3-jetson-net`
    * `./jetson_ubuntu/face_reg.py` is executed in this container to scan videos, detect faces, and publish binary messages to a local MQTT broker `jetson_mqtt_broker`.
2. jetson_mqtt_broker
    * Built using `./jetson_mqtt_broker/Dockerfile`
    * Attached to a user-defined network called `hw3-jetson-net`
    * `./jetson_mqtt_broker/mosquitto.conf` is executed in this container.
3. jetson_mqtt_forwarder
    * Built using `./jetson_mqtt_forwarder/Dockerfile`
    * Attached to a user-defined network called `hw3-jetson-net`
    * `./jetson_mqtt_forwarder/mqtt_subscriber_local.py` is executed in this container to subscribe messages and publish them to a Cloud MQTT broker `ibm_mqtt_broker`, whose public IP is `52.117.20.245`.
4. ibm_mqtt_broker
    * Built using `./ibm_mqtt_broker/Dockerfile`
    * Attached to a user-defined network called `hw3-ibm-net`
    * `./ibm_mqtt_broker/mosquitto.conf` is executed in this container.
5. ibm_ubuntu
    * Built using `./ibm_ubuntu/Dockerfile`
    * Attached to a user-defined network called `hw3-ibm-net`
    * Directory `/mnt/mybucket` is FUSE mounted onto [a bucket](https://cos-w251-standard-hw3.s3.us-south.cloud-object-storage.appdomain.cloud)
    * `./ibm_ubuntu/mqtt_subscriber_remote.py` is executed in this container to subscribe messages, decode messages and save them in the bucket.
