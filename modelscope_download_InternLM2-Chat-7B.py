# https://modelscope.cn/models/Shanghai_AI_Laboratory/internlm2-chat-7b/summary
# https://github.com/InternLM/tutorial/blob/main/helloworld/hello_world.md#22-%E6%A8%A1%E5%9E%8B%E4%B8%8B%E8%BD%BD

import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os

# model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-7b', cache_dir='/root/model', revision='v1.0.3')
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-7b', cache_dir='/root/model')