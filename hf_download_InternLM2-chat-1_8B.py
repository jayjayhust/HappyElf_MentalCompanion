# https://github.com/InternLM/tutorial/blob/main/langchain/readme.md#13-langchain-%E7%9B%B8%E5%85%B3%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE

# pip install -U huggingface_hub

import os

# 设置环境变量(huggingface 镜像下载)
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载模型
os.system('huggingface-cli download --resume-download internlm/internlm2-chat-1_8b --local-dir ./model/internlm2-chat-1_8b')