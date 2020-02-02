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
  * Max pooling layer
  * Convolution layer
  * Max pooling layer
  * Output layer
* Experiment with the number and size of filters in each layer. Does it improve the accuracy?
* Remove the pooling layers. Does it impact the accuracy?
* Add one more conv layer. Does it help with accuracy?
* Increase the batch size. What impact does it have?
* What is the best accuracy you can achieve? Are you over 99%? 99.5%?
