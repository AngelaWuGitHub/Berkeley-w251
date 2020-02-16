## Homework 7 - Neural Face Detection Pipeline

I modified [the processing pipeline implemented in HW3](https://github.com/AngelaWuGitHub/Berkeley-w251/tree/master/HW3) and replaced the OpenCV-based face detector with a Mobilenet-SSD face detector. 

I made three modifications in total:
* I created a new container `my_ubuntu6` for face detection (see details in the next section)
* I modified the `face_reg.py` to use a Mobilenet-SSD face detector. I kept OpenCV Haarcascade face detector for runtime and accuracy comparison. The modified `face_reg.py` is included in this repo.
* I modified `ibm_ubuntu` container in HW3 and saved thes image in `s3fs cos-w251-standard-hw7` instead of `s3fs cos-w251-standard-hw3`.

Container used for face detection (in replace of jetson_ubuntu in HW3):
* `sudo docker run --name my_ubuntu6 --network hw3-jetson-net --device /dev/video1:/dev/video1 --privileged -dit -d w251/tensorflow:dev-tx2-4.3_b132-tf1 bash`
* Installed OpenCV following https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
* Installed `curl`, `mosquitto-clients`, and `wget`  
    `apt-get install -y curl mosquitto-clients wget`
* pip installed `paho-mqtt`  
    `pip3 instal paho-mqtt`
* Downloaded OpenCV Haarcascade for comparison:  
    `curl -o haarcascade_frontalface_default.xml \
    'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'`
* Downloaded Mobilenet-SSD model:  
    `wget https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true -O data/frozen_inference_graph_face.pb`

**My answers to the homework questions**:
* Describe your solution in detail. What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
    * I followed the [sample notebook](https://github.com/MIDS-scaling-up/v2/blob/master/week07/hw/hw07-hint.ipynb) that loads and uses [one face detector](https://github.com/yeephycho/tensorflow-face-detection). It uses a mobilenet SSD (single shot multibox detector) based face detector with pretrained model provided, powered by tensorflow object detection api, trained by WIDERFACE dataset. 
    * Based on this blog (https://medium.com/nodeflux/performance-showdown-of-publicly-available-face-detection-model-7c725747094a), Mobilenet-SSD face detector can achieve a mean average precision of 72%.
* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
    * In my empirical tests, the Mobilenet-SSD didn't perform as well as OpenCV. OpenCV was able to capture faces that the Mobilenet-SSD face detector cannot, and it was faster to run (see my responses for the next two questions for runtime comparison). So I would not use this to develop a robust production-grade system.
* What framerate does this method achieve on the Jetson? Where is the bottleneck?
    * It takes approximately 0.09 seconds for the Mobilenet-SSD face detector to detect face(s). So the framerate is around 10 per second.
* Which is a better quality detector: the OpenCV or yours?
    * It takes approximately 0.05 seconds for OpenCV to detect face(s), twice as fast as the neural face detector.
    
**Detected Face Images**:  
Currently there are 26 faces saved in my bucket. The public URL to each of those faces follows the format `https://cos-w251-standard-hw7.s3.us-south.cloud-object-storage.appdomain.cloud/MyFace-<number>.jpg`. `<number>` ranges from 0 to 25.  
For example, the public URL for the 11th face saved is `https://cos-w251-standard-hw7.s3.us-south.cloud-object-storage.appdomain.cloud/MyFace-10.jpg`.  

I also saved one example of my face in this repo.  

![Example 1](MyFace-10.jpg)
