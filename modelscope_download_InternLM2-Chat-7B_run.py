# https://modelscope.cn/models/Shanghai_AI_Laboratory/internlm2-chat-7b/summary
# https://github.com/InternLM/tutorial/blob/main/helloworld/hello_world.md#22-%E6%A8%A1%E5%9E%8B%E4%B8%8B%E8%BD%BD

from modelscope import snapshot_download, AutoTokenizer, AutoModelForCausalLM
import torch

model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-7b', cache_dir='/root/model')
tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", trust_remote_code=True)
# Set `torch_dtype=torch.float16` to load model in float16, otherwise it will be loaded as float32 and might cause OOM Error.
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto",  trust_remote_code=True, torch_dtype=torch.float16)
model = model.eval()
response, history = model.chat(tokenizer, "hello", history=[])
print(response)
# Hello! How can I help you today?
response, history = model.chat(tokenizer, "please provide three suggestions about time management", history=history)
print(response)