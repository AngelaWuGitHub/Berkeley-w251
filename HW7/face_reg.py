import cv2
import paho.mqtt.client as mqtt

print(cv2.getBuildInformation())

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv2.VideoCapture(1)

print('Video device connection status: ', cap.isOpened())

# To set the resolution
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Arguments for the publisher
LOCAL_MQTT_BROKER = "jetson_mqtt_broker"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "hw3_topic/local"
# Default flag
flag_connected = 0
# It's hard to visually tell a face with a gray scaled picture in my case
#   so I kept the original picture color
# Gray-scaled or not
gray_scale = False


# Reference: https://stackoverflow.com/questions/36093078/mqtt-is-there-a-way-to-check-if-the-client-is-still-connected
def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1


def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0


# Connect to broker
client = mqtt.Client()
print('----------- Checkpoint 1 -----------')
client.connect(LOCAL_MQTT_BROKER, LOCAL_MQTT_PORT, 60)
print('----------- Checkpoint 2 -----------')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
# loop_start() vs. loop_forever():
#   http://www.steves-internet-guide.com/loop-python-mqtt-client/
client.loop_start()

# find -name "haarcascades"
# my_ubuntu4
# face_cascade = cv2.CascadeClassifier('/root/opencv-4.2.0/data/haarcascades/haarcascade_frontalface_default.xml')
# is_load = face_cascade.load('/root/opencv-4.2.0/data/haarcascades/haarcascade_frontalface_default.xml')

# my_ubuntu1
# ./root/opencv_build/opencv/data/haarcascades
# ./usr/local/share/opencv4/haarcascades
# face_cascade = cv2.CascadeClassifier('/root/opencv_build/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
# is_load = face_cascade.load('/root/opencv_build/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

# jetson_ubuntu
# Downloaded from 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
is_load = face_cascade.load('haarcascade_frontalface_default.xml')

if is_load:
    print('Load haarcascades successfully')
else:
    print('Fail to load haarcascades')

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(frame.shape)
    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    # cv2.imshow('Preview', gray)

    if gray_scale:
        frame_used = gray
    else:
        frame_used = frame
    # Face detection
    faces = face_cascade.detectMultiScale(frame_used, 1.3, 5)
    if len(faces) > 0:
        print('---------------- Face(s) detected')
    else:
        print('No face detected')

    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame_used, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cut out face from the frame..
        face_detected = frame_used[y:y + h, x:x + w]
        # cv2.imshow('Preview Face', face_detected)
        rc, png = cv2.imencode('.png', face_detected)
        if rc:
            print('Encode successfully')
        msg = png.tobytes()
        # Reference: https://stackoverflow.com/questions/17967320/python-opencv-convert-image-to-byte-string
        # msg = png.tostring()

        # Publish a message
        if flag_connected == 1:
            print('Publishing messages')
            client.publish(LOCAL_MQTT_TOPIC, msg)
        else:
            print('No connection to MQTT broker')

    # Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client.disconnect()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
