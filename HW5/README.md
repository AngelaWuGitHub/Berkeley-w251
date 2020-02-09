## Homework 5 - TF2 and TF1

### Introduction to Tensorflow v2

TF2 beginner lab:
* beginner.ipynb - the original Jupyter Notebook downloaded from https://www.tensorflow.org/tutorials/quickstart/beginner
* beginner_my_run.ipynb - my run of the same Jupyter Notebook
   * The structure of the network: a dense layer of 128 nodes with 20% dropout and an output layer to classify 10 classes
   * Validation accuracy is 0.9764
* beginner_improved.ipynb - I improved the network by adding two convoluation layers and two max pooling layer
   ```
   tf.keras.layers.Reshape(input_shape=(28,28,), target_shape=[28,28,1]),  
   tf.keras.layers.Conv2D(16, kernel_size=(3,3), padding='same', activation='relu'),  
   tf.keras.layers.MaxPooling2D(pool_size=(2,2)),  
   tf.keras.layers.Conv2D(32, kernel_size=(3,3), padding='same', activation='relu'),  
   tf.keras.layers.MaxPooling2D(pool_size=(2,2)),  
   tf.keras.layers.Dropout(0.2),  
   tf.keras.layers.Flatten(),  
   tf.keras.layers.Dense(128, activation='relu'),  
   tf.keras.layers.Dropout(0.2),  
   tf.keras.layers.Dense(10, activation='softmax')
   ```
   * Validation accuracy is 0.9897
   
TF2 Quickstart lab:
* transfer_learning_with_hub.ipynb - the original Jupyter Notebook downloaded from https://www.tensorflow.org/tutorials/images/transfer_learning_with_hub
* transfer_learning_with_hub_my_run.ipynb - my run of the same Jupyter Notebook
   * I reduced the batch size from 32 to 16 to fix the OOM error.
   * I classified 15 out 16 `image_batch` pictures correctly.
* transfer_learning_with_hub_improved.ipynb - I improved the network by adding additional dense layer
   ```
   feature_extractor_layer,
   layers.Dense(256, activation='relu'),
   layers.Dense(image_data.num_classes, activation='softmax')
   ```
   * I classified 16 out 16 `image_batch` pictures correctly.


### Introduction to / Comparison with Tensorflow v1

To resolve the OOM error, I had to:
* Run `flush_buffers.sh`
* Run the following in the python3 terminal
    ```
    import tensorflow as tf
    tf.reset_default_graph()
    ```
    
    
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
    * A bottleneck is a layer before the output layer that has the most dense representation of the input layer.
* How is a bottleneck different from the concept of layer freezing?
    * Input => Freezed-Layers => Last-Layer-To-Re-Compute => Output
    * To train Last-Layer-To-Re-Compute, we need to evaluate outputs of Freezed-Layers multiple times for a given input data. In order to save time, we save the bottleneck values (i.e., outputs of Freezed-Layers) for each image.
* In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
    * The lab analyzes every image through MobileNet except for its original output layer and calculates its bottleneck values. Then the lab uses the bottleneck values to train the last layer using the images in `tf_files_dir`. 
* How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
    * The default learning rate is 0.01. Learning rate of 0.005 took a tiny bit longer to run (i.e., runtime increased from 17 min to 18 min), and the accuracy increased from 89% to 90.6%. 
    * _Note_: My answer does NOT include the time to save bottleneck values
* How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?
    * Test accuracy is 89.5%. It's good enough to produce a usable graph.
* For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
    * I downloaded 60 images, 30 for lions and 30 for tigers. I got test accuracy of 83.3% with only 40 steps. So I was able to train a decent model with a small number of images.
* Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
    * It was faster to train on CPU (12 min) than to train on GPU (17min). My guess is GPU is more powerful on a bigger neural network and all I need to train here is the output layer, so CPU is more effective.
    * _Note_: My answer does NOT include the time to save bottleneck values
* Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?
    * Similar to MobileNet model, it was faster to train on CPU (17 min) than to train on GPU (31 min).
    * _Note_: My answer does NOT include the time to save bottleneck values
* Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?
    * ```python -m scripts.label_image --input_layer="Mul" --input_height=299 --input_width=299  --graph=tf_files/retrained_graph.pb --image=tf_files/flower_photos/daisy/21652746_cc379e0eea_m.jpg```
