# conda install pytorch torchvision torchaudio -c pytorch
# pip3 install tensorflow  

import torch
from aitextgen import aitextgen # wrapper for gpt2 text gen
from transformers import GPT2LMHeadModel, GPT2Tokenizer 

def sequenceExtend(prompt_text, max_length = 100, top_k=50):
    # Instantiate the model
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    # Encode / embed into vector space
    inputs = tokenizer.encode(prompt_text, return_tensors='pt')
    outputs = model.generate(inputs
                            ,max_length=max_length
                            ,do_sample=True
                            ,temperature=1
                            ,top_k=50)
                            
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
    

def sequenceExtend_aitextgen(prompt_text, max_length=100, tf_gpt2="124M"):
    """
    Args:
        prompt_text (str): Input text for extension by GPT-2.
        max_length (int): Maximum length of the output text.
        tf_gpt2 (str): The valid TF model names - ["124M", "355M", "774M", "1558M"]
    Return:
        str: An extended version of the input_text
    Ref: https://www.youtube.com/watch?v=nka_X7bDH-w
    """
    ai = aitextgen() # Instantiate the model
    return ai.generate_one(prompt=prompt_text, max_length=max_length)


def demoGPT2(model="aitextgen"):
    prompt_text = "Python is awesome!"

    if model == "aitextgen":
        gpt_text = sequenceExtend_aitextgen(prompt_text)

    elif model == "original":
        gpt_text = sequenceExtend(prompt_text)

    print(gpt_text)

