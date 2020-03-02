## Homework 9 - Distributed Training and Neural Machine Translation


nohup.out file is saved in this repo ([link](nohup.out)).

1. How long does it take to complete the training run?  
I used a pair of P-100 VMs (i.e., AC1_16X120X100) and it took 26 hours, 23 minutes, and 36 seconds to run 50k steps.  

2. Do you think your model is fully trained? How can you tell?  
I think my model is close to (but not yet) fully trained. The evaluation loss had been decreasing and started to level off at 50k steps. The evaluation BLEU had been increasing and the growth was slowier toward the end.
![Eval Loss](https://github.com/AngelaWuGitHub/Berkeley-w251/blob/master/HW9/Screenshots/TensorBoard%20Screenshot%20eval_loss.PNG)
![Eval BLEU](https://github.com/AngelaWuGitHub/Berkeley-w251/blob/master/HW9/Screenshots/TensorBoard%20Screenshot%20Eval_BLEU_Score.PNG)

3. Were you overfitting?  
The evaluation loss kept decreasing, so I don't think the model overfitted.

4. Were your GPUs fully utilized?  
Two screenshots (one for p100a and the other for p100b) below show that 4 GPUs were all 100% utilized.  
![p100a GPU](https://github.com/AngelaWuGitHub/Berkeley-w251/blob/master/HW9/Screenshots/Screenshot%20nvidia-smi%20p100a.PNG)
![p100b GPU](https://github.com/AngelaWuGitHub/Berkeley-w251/blob/master/HW9/Screenshots/Screenshot%20nvidia-smi%20p100b.PNG)

5. Did you monitor network traffic (hint: `apt install nmon`) ? Was network the bottleneck?  
The receive and transimit throughput ranged from 180 Mbps to 210 Mbps (see screenshot below) while the max port speed for p100 is 1000 Mbps. Network was not the bottleneck. GPU was the bottleneck.  
![p100a network](https://github.com/AngelaWuGitHub/Berkeley-w251/blob/master/HW9/Screenshots/Screenshot%20nmon.PNG)

6. Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?  
Below is a screenshot of the learning rate plot from TensorBoard.  
![Learning Rate](https://github.com/AngelaWuGitHub/Berkeley-w251/blob/master/HW9/Screenshots/TensorBoard%20Screenshot%20learning_rate.PNG)

Based on the screenshot above, the learning rate seems to increase linearly and then decay exponentially.  
After reviewing [transformer-base.py](https://github.com/NVIDIA/OpenSeq2Seq/blob/master/example_configs/text2text/en-de/transformer-base.py) and [lr_policies.py](https://github.com/NVIDIA/OpenSeq2Seq/blob/master/open_seq2seq/optimizers/lr_policies.py), I found the learning rate is calculated as:  
```math
xxxxx
```

7. How big was your training set (mb)? How many training lines did it contain?  
`/data/wmt16_de_en/train.clean.en.shuffled.BPE_common.32K.tok` is 959MB and contains 4,524,868 lines.

8. What are the files that a TF checkpoint is comprised of?  
  TF checkpoint is comprised of three files:  
  * `model.ckpt-<step>.data-00000-of-00001`
  * `model.ckpt-<step>.index`
  * `model.ckpt-<step>.meta`

9. How big is your resulting model checkpoint (mb)?  
  * `model.ckpt-<step>.data-00000-of-00001`: 731MB
  * `model.ckpt-<step>.index`: 1MB
  * `model.ckpt-<step>.meta`: 13MB

10. Remember the definition of a "step". How long did an average step take?


11. How does that correlate with the observed network utilization between nodes?

