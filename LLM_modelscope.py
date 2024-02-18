from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from modelscope import snapshot_download, AutoTokenizer, AutoModelForCausalLM
import torch
import const

class InternLM_LLM(LLM):
    # 基于本地 InternLM 自定义 LLM 类

    def __init__(self, model_path :str, cache_path :str = '/root/model'):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        super().__init__()
        print("正在从本地加载模型...")
        # model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-7b', cache_dir='/root/model')
        model_dir = snapshot_download(model_path, cache_dir=cache_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", trust_remote_code=True)
        # Set `torch_dtype=torch.float16` to load model in float16, otherwise it will be loaded as float32 and might cause OOM Error.
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto",  trust_remote_code=True, torch_dtype=torch.float16).cuda()
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self, prompt : str, stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = None,
                **kwargs: Any):
        # 重写调用函数
        # system_prompt = """你是一个心理医生小助手，负责倾听用户的心理问题并给出建议."""
        system_prompt = const.CHARACTER_DESCRIPTION
        messages = [(system_prompt, '')]
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        return response
    
    def generate(self, prompt : str, stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = None,
                **kwargs: Any):
        # 重写调用函数
        system_prompt = """你是一个心理医生小助手，负责倾听用户的心理问题并给出建议.
        """
        
        messages = [(system_prompt, '')]
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "InternLM"