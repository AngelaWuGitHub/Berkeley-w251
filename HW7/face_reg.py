import cv2
import paho.mqtt.client as mqtt

import sys
import os
# tf.contrib doesn't exist in 2.0.
import tensorflow.contrib.tensorrt as trt
# Code below works with TF2
# from tensorflow.python.compiler.tensorrt import trt_convert as trt
import tensorflow as tf
import numpy as np
import time

print(cv2.getBuildInformation())

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv2.VideoCapture(1)

print('Video device connection status: ', cap.isOpened())
# Capture frame per second
fps = int(cap.get(cv2.CAP_PROP_FPS))
print('-------------------------------------- fps: {}'.format(fps))

# To set the resolution
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

# Download an SSD model for face detection
# https://github.com/yeephycho/tensorflow-face-detection
FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'

# Load the frozen graph
output_dir = ''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
    frozen_graph.ParseFromString(f.read())
# https://github.com/NVIDIA-AI-IOT/tf_trt_models/blob/master/tf_trt_models/detection.py
INPUT_NAME = 'image_tensor'
BOXES_NAME = 'detection_boxes'
CLASSES_NAME = 'detection_classes'
SCORES_NAME = 'detection_scores'
MASKS_NAME = 'detection_masks'
NUM_DETECTIONS_NAME = 'num_detections'
input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

# Optimize the frozen graph using TensorRT
trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

# Create session and load graph
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True
tf_sess = tf.Session(config=tf_config)
# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')
# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')
tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')

# OpenCV CascadeClassifier
# Downloaded from 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
is_load = face_cascade.load('haarcascade_frontalface_default.xml')

if is_load:
    print('Load haarcascades successfully')
else:
    print('Fail to load haarcascades')

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

count = 0
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Only capture 1 face per second
    # if count % (1 * fps) != 0:
    #     continue
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
    print('======================================== OpenCV ====================================')
    t0 = time.time()
    faces = face_cascade.detectMultiScale(frame_used, 1.3, 5)
    t1 = time.time()
    print('Face Detection Runtime: %f seconds' % float(t1 - t0))

    if len(faces) > 0:
        print('---------------- Face(s) detected')
    else:
        print('No face detected')

    for (x, y, w, h) in faces:
        print('rectangle', x, y, w, h)
        # # Draw a rectangle around the face
        # # cv2.rectangle(image, start_point, end_point, color, thickness)
        # cv2.rectangle(frame_used, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # # cut out face from the frame..
        # face_detected = frame_used[y:y + h, x:x + w]
        # # cv2.imshow('Preview Face', face_detected)
        # rc, png = cv2.imencode('.png', face_detected)
        # if rc:
        #     print('Encode successfully')
        # msg = png.tobytes()
        # # Reference: https://stackoverflow.com/questions/17967320/python-opencv-convert-image-to-byte-string
        # # msg = png.tostring()
        #
        # # Publish a message
        # if flag_connected == 1:
        #     print('Publishing messages')
        #     client.publish(LOCAL_MQTT_TOPIC, msg)
        # else:
        #     print('No connection to MQTT broker')

    print('======================================== tf_trt_models ====================================')
    # Reference: https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    t0 = time.time()
    image_resized = np.array(cv2.resize(frame_used, (300, 300), interpolation=cv2.INTER_AREA))
    t1 = time.time()
    print('Resizing Runtime: %f seconds' % float(t1 - t0))

    # Run network on image
    t0 = time.time()
    scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections],
                                                         feed_dict={
                                                             tf_input: image_resized[None, ...]
                                                         })

    boxes = boxes[0]  # index by 0 to remove batch dimension
    scores = scores[0]
    classes = classes[0]
    num_detections = num_detections[0]
    t1 = time.time()
    print('Face Detection Runtime: %f seconds' % float(t1 - t0))

    print('Number of potential faces detected: ', num_detections)

    # suppress boxes that are below the threshold..
    DETECTION_THRESHOLD = 0.5
    # if int(num_detections) == 0:
    #     print('No face detected')

    for i in range(int(num_detections)):
        if scores[i] < DETECTION_THRESHOLD:
            # print('Confidence low')
            continue

        print('---------------- Face(s) detected')
        # scale box to image coordinates
        box = boxes[i] * np.array([frame_used.shape[0], frame_used.shape[1], frame_used.shape[0], frame_used.shape[1]])
        print('rectangle', box[1], box[0], box[3], box[2])
        # display rectangle
        # cv2.rectangle(image, start_point, end_point, color, thickness)
        cv2.rectangle(frame_used, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (255, 0, 0), 2)
        face_detected = frame_used[int(box[0]):int(box[2]), int(box[1]):int(box[3])]
        rc, png = cv2.imencode('.png', face_detected)
        if rc:
            print('Encode successfully')
        msg = png.tobytes()

        # Publish a message
        if flag_connected == 1:
            print('Publishing messages')
            client.publish(LOCAL_MQTT_TOPIC, msg)
        else:
            print('No connection to MQTT broker')

    count += 1
    # Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client.disconnect()

# close tf session
tf_sess.close()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
