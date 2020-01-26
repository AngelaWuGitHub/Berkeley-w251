import paho.mqtt.client as mqtt

# This is the Subscriber
LOCAL_MQTT_BROKER = "jetson_mqtt_broker"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "hw3_topic/local"
REMOTE_MQTT_BROKER = "52.117.20.245"
REMOTE_MQTT_PORT = 1883
REMOTE_MQTT_TOPIC = "hw3_topic/remote"


def on_connect_local(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        print("Message received")
        # if we wanted to re-publish this message, something like this should work
        msg = msg.payload
        client_remote.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    except:
        print('Message not received')
    # if msg.payload.decode() == "Hello world!":
    #     print("Yes!")
    #     client.disconnect()


client_local = mqtt.Client()
client_local.connect(LOCAL_MQTT_BROKER, LOCAL_MQTT_PORT, 60)

client_local.on_connect = on_connect_local
client_local.on_message = on_message

client_remote = mqtt.Client()
client_remote.connect(REMOTE_MQTT_BROKER, REMOTE_MQTT_PORT, 60)

client_local.loop_forever()