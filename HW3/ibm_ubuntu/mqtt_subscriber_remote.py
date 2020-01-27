import paho.mqtt.client as mqtt
import numpy as np
import cv2

# This is the Subscriber
IBM_MQTT_BROKER = "ibm_mqtt_broker"
IBM_MQTT_PORT = 1883
IBM_MQTT_TOPIC = "hw3_topic/remote"
counter = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(IBM_MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        print("Message received")
        global counter
        # Test saving files
        # file = open("/mnt/mybucket/testfile-{}.txt".format(counter), "w")
        # file.write("Message received")
        # file.close()
        # if msg = png.tostring() is used in face_reg.py
        # then use buff = np.fromstring(msg.payload, np.uint8)
        # if msg = png.tobytes() is used in face_reg.py
        # then use the following
        buff = np.frombuffer(msg.payload, dtype=np.uint8)
        buff = buff.reshape(1, -1)
        img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
        cv2.imwrite("/mnt/mybucket/MyFace-{}.jpg".format(counter), img)
        counter += 1
    except:
        print('Message not received')


client = mqtt.Client()
client.connect(IBM_MQTT_BROKER, IBM_MQTT_PORT, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()