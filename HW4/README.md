## Homework 4 - DL 101

### 2. ConvnetJS MNIST demo
http://cs.stanford.edu/people/karpathy/convnetjs/demo/mnist.html

Default model:  
```
layer_defs = [];
layer_defs.push({type:'input', out_sx:24, out_sy:24, out_depth:1});
layer_defs.push({type:'conv', sx:5, filters:8, stride:1, pad:2, activation:'relu'});
layer_defs.push({type:'pool', sx:2, stride:2});
layer_defs.push({type:'conv', sx:5, filters:16, stride:1, pad:2, activation:'relu'});
layer_defs.push({type:'pool', sx:3, stride:3});
layer_defs.push({type:'softmax', num_classes:10});

net = new convnetjs.Net();
net.makeLayers(layer_defs);

trainer = new convnetjs.SGDTrainer(net, {method:'adadelta', batch_size:20, l2_decay:0.001});
```

* Name all the layers in the network, make sure you understand what they do.
  * Input layer
      * A single raw image is given as an input. 
      * In this demo, each image is 24x24 black and white, so the input dimension is 24x24x1.
  * Convolution layer
    * A filter, smaller than the input image, is moved across the image with a certain stride. Every time it moves, it performs a matrix multiplication between the portion of the image it hovers over and the filter weights. Padding is used to add additional blank pixels to the border of an image so that information on the edges/corners of the image is not lost or counted less often.
    * In the default code of this demo, each filter is 5x5, and it moves across the image one pixel at a time (stride=1). Two additional blank pixels are added to the border of the image (pad=2). There are in total of 8 filters in this layer. The activation function is relu. The output dimension of this layer is 24x24x8.
  * Max pooling layer
    * Pooling layer is used to extract dominant features. In ConvNetJS, it performs max pooling. Max pooling returns the maximum value from the portion of the image a filter hovers over.
    * In the default code of this demo, each filter is 2x2, and it moves across the image two pixels at a time (Stride=2). The output dimension of this layer is 12x12x8.
  * Convolution layer
    * In the default code of this demo, each filter is 5x5, and it moves across the image one pixel at a time (stride=1). Two additional blank pixels are added to the border of the image (pad=2). There are in total of 16 filters in this layer. The activation function is relu. The output dimension of this layer is 12x12x16
  * Max pooling layer
    * In the default code of this demo, each filter is 3x3, and it moves across the image three pixels at a time (Stride=3). The output dimension of this layer is 4x4x16.
  * Output layer
    * The output layer is a fully connected layer that is used to predict a set of discrete classes. In softmax, the outputs are probabilities that sum to 1.
    * In this demo, we are trying to predict hand-written digits from 0 to 9. So the number of classes is equal to 10.
* Experiment with the number and size of filters in each layer. Does it improve the accuracy?
* Remove the pooling layers. Does it impact the accuracy?
* Add one more conv layer. Does it help with accuracy?
* Increase the batch size. What impact does it have?
* What is the best accuracy you can achieve? Are you over 99%? 99.5%?
