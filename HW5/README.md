## Homework 5 - TF2 and TF1

### Introduction to Tensorflow v2


### Introduction to / Comparison with Tensorflow v1


### Questions

* What is TensorFlow? Which company is the leading contributor to TensorFlow?
    * TensorFlow is an open source package for numerical computation and deep learning.
    * Google is the leading contributor to TensorFlow
* What is TensorRT? How is it different from TensorFlow?
    * NVIDIA TensorRT is a high-performance inference optimizer. It speeds up deep learning inference through optimizations and high-performance runtimes for GPU-based platforms. 
    * NVIDIA TensorRT can only be used to perform inference. In contrast, TensorFlow can train a deep learning model as well as perform inference using the model.
* What is ImageNet? How many images does it contain? How many classes?
    * ImageNet is an image database of 14,197,122 images. 
    * ImageNet is organized according to the WordNet hierarchy, where each meaningful concept is called "synset". There are a total of 21,841 non-empty synsets (i.e., classes) in the ImageNet.
    * Here is a link to other statistics about ImageNet: http://image-net.org/about-stats (updated on April 30, 2010)
* Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
    * GoogleNet (an inception network): apply 1x1 pointwise convolution first to reduce dimensions and then apply multiples of 3x3, 5x5, etc. convolution layers to the same input layer
    * MobileNet (an Xception network): apply channel-wise (i.e., depthwise) nxn convolution (depth of 1) and then apply 1x1 pointwise convolution
* In your own words, what is a bottleneck?
    * A bottleneck is a 1x1 pointwise convolution layer that's designed to "collapse" feature maps and reduce dimensions.
* How is a bottleneck different from the concept of layer freezing?
    * Both bottleneck layers and layer freezing reduces the number of parameters in a neural network. When a layer is frozen, the weights for that layer are updated. On the other hand, the weights for the bottleneck layer are updated.
* In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
* How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
* How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?
* For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
* Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
* Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?
Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?
