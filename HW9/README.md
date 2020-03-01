## Homework 9 - Distributed Training and Neural Machine Translation


nohup.out file is saved in this repo.[INSERT LINK TO NOHUP.OUT HERE]

1. How long does it take to complete the training run?  
I used a pair of P-100 VMs (i.e., AC1_16X120X100) and it took about 26 and a half hours to run 50k steps.  

2. Do you think your model is fully trained? How can you tell?  
I think my model is close to fully trained. The evaluation loss had been decreasing and started to level off around 45k steps.  
[INSERT EVAL LOSS SCREENSHOT HERE]

3. Were you overfitting?  
The evaluation loss did not hit the bottom and increase yet, so I don't think the model overfitted.

4. Were your GPUs fully utilized?  
Two screenshots (one for p100a and the other for p100b) below show that 4 GPUs were all 100% utilized.  
[INSERT TWO NVIDIA-SMI SCREENSHOTS HERE]

5. Did you monitor network traffic (hint: `apt install nmon`) ? Was network the bottleneck?


6. Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?
Below is a screenshot of the learning rate plot from TensorBoard.  
[INSERT LEARNING RATE SCREENSHOT HERE]  
Based on the screenshot above, the learning rate seems to increase linearly and then decay exponentially.  
After reviewing [transformer-base.py](https://github.com/NVIDIA/OpenSeq2Seq/blob/master/example_configs/text2text/en-de/transformer-base.py) and [lr_policies.py](https://github.com/NVIDIA/OpenSeq2Seq/blob/master/open_seq2seq/optimizers/lr_policies.py), I found the learning rate is calculated as:  
```math
xxxxx
```

7. How big was your training set (mb)? How many training lines did it contain?


8. What are the files that a TF checkpoint is comprised of?


9. How big is your resulting model checkpoint (mb)?


10. Remember the definition of a "step". How long did an average step take?


11. How does that correlate with the observed network utilization between nodes?

