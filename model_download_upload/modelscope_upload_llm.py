# https://modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E7%9A%84%E4%B8%8A%E4%BC%A0
# configuration.json示例：https://modelscope.cn/models/qwen/Qwen1.5-7B-Chat/file/view/master/configuration.json?status=1

# 还是推荐用git上传模型，测试了sdk上传报错
# 过程记录（假设自己已经在modelscope上创建了my_test_model模型库）：
# git lfs install
# git clone https://www.modelscope.cn/user/my_test_model.git
# cd my_test_model
# cp -rf /work/my_model_dir/* .  # 复制模型文件到当前目录（假设你的模型文件位于/work/my_model_dir目录下）
# git add -A .
# git commit -m "commit message"
# git push

from modelscope.hub.api import HubApi
import os

YOUR_ACCESS_TOKEN = os.getenv("modelscope_api_key")  # 请替换成你的环境变量

api = HubApi()
api.login(YOUR_ACCESS_TOKEN)
api.push_model(
    model_id="jayhust/internlm2-chat-1_8b", 
    model_dir="./model/internlm2-chat-1_8b",  # 本地模型目录，要求目录中必须包含configuration.json
    license="Apache-2.0",  # 模型许可证
    chinese_name="书生·浦语2-chat-1.8b",  # 模型名称
    tag="chat,language model"  # 模型标签
)