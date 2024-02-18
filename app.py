# homework for lesson3：选择一个垂直领域，收集该领域的专业资料构建专业知识库，并搭建专业问答助手，并在 OpenXLab 上成功部署（截图，并提供应用地址）
# OpenXLab部署应用注意：
# 1.应用默认的启动文件为关联代码仓库根目录下的 app.py 文件 app.py 示例
# 2.配置应用所需的运行环境，如有 Python 依赖项（pip 安装）可写入 requirements.txt 中，Debian 依赖项（apt-get 安装）可写入 packages.txt 中，并存放至代码仓库的根目录下
# 3.如需提高应用中模型文件下载速度，建议尝试 模型托管
# 4.应用默认在 7860 端口启动，请不要占用或改写个人应用的启动端口


from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import os
from LLM import InternLM_LLM as LLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import const

def load_chain():
    """
    加载问答链(RAG)
    
    Args:
        无
    
    Returns:
        RetrievalQA: 问答链实例
    """
    # 加载问答链
    # 定义 Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="/root/model/sentence-transformer")

    # 向量数据库持久化路径
    persist_directory = 'data_base/vector_db/chroma'

    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
        embedding_function=embeddings
    )

    # 加载自定义 LLM
    llm = LLM(model_path = "/root/model/Shanghai_AI_Laboratory/internlm-chat-7b")

    # 定义一个 Prompt Template
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    有用的回答:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    # 运行 chain
    qa_chain = RetrievalQA.from_chain_type(llm, 
                                           retriever=vectordb.as_retriever(),  # 设置召回器为 vectordb
                                           return_source_documents=True, 
                                           chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
    
    return qa_chain

def get_dialogue_history(dialogue_history_list: list):   
    dialogue_history_tmp = []

    for item in dialogue_history_list:
        if item['role'] == 'counselor':
            text = '咨询师：'+ item['content']
        else:
            text = '来访者：'+ item['content']
        dialogue_history_tmp.append(text)

    dialogue_history = '\n'.join(dialogue_history_tmp)
    
    return dialogue_history + '\n' + '咨询师：'

def get_instruction(dialogue_history):
    instruction = const.CHARACTER_DESCRIPTION + \
        "\n\n对话：" + dialogue_history

    return instruction

class Model_center():
    """
    存储LLM或者检索问答链的对象
    """
    def __init__(self, llm_path=None):
        # 构造函数，加载检索问答链
        # self.chain = load_chain()
        # 加载自定义 LLM
        # llm = LLM(model_path = "/root/model/Shanghai_AI_Laboratory/internlm2-chat-7b")  # intern-studio pc: download to linux
        # self.llm = LLM(model_path = "./model/internlm2-chat-1_8b")  # local pc: download to windows
        self.llm = LLM(model_path = llm_path)  # huggingface model hub
        self.dialogue_history_list = []

    def qa_chain_self_answer(self, question: str, chat_history: list = []):
        """
        调用问答链进行回答
        """
        if question == None or len(question) < 1:
            return "", chat_history
        try:
            chat_history.append((question, self.chain({"query": question})["result"]))
            # 将问答结果直接附加到问答历史中，Gradio 会将其展示出来
            return "", chat_history
        except Exception as e:
            return e, chat_history
    
    def clear_chat_history(self):
        """
        清空聊天历史记录
        """
        self.dialogue_history_list = []

    def direct_answer(self, prompt: str, chat_history: list = []):
        self.dialogue_history_list.append({  # 聊天记录中附加用户的输入
            'role': 'client',
            'content': prompt
        })
        dialogue_history = get_dialogue_history(dialogue_history_list=self.dialogue_history_list)
        instruction = get_instruction(dialogue_history=dialogue_history)  # 生成提示词
        response = self.llm.generate(instruction)
        print(f'咨询师：{response}')
        self.dialogue_history_list.append({  # 聊天记录中附加大模型的返回结果
            'role': 'counselor',
            'content': response
        })

        chat_history.append((prompt, response))
        return "", chat_history

import gradio as gr

# 设置环境变量(huggingface 镜像下载)
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# 先下载模型到本地
# os.system('huggingface-cli download --resume-download internlm/internlm2-chat-1_8b --local-dir ./model/internlm2-chat-1_8b')
os.system('huggingface-cli download --resume-download internlm/' + const.LLM_NAME + ' --local-dir ./model/' + const.LLM_NAME)

# 实例化核心功能对象
model_center = Model_center(llm_path='./model/' + const.LLM_NAME)

# 创建一个 Web 界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):   
        with gr.Column(scale=15):
            # 展示的页面标题
            # 图片链接(github)：https://raw.githubusercontent.com/jayjayhust/HappyElf_MentalCompanion/main/assets/images/happy_little_elf-round.png
            # 图片链接(gitee)：https://gitee.com/hunan_ai_league_jayhust/resource_storage/raw/master/happy_little_elf-round.png
            gr.Markdown("""<h1><center>Happy Little Elf</center></h1>
                <center>快乐小精灵</center>
                <br>
                <center><img src="https://raw.githubusercontent.com/jayjayhust/HappyElf_MentalCompanion/main/assets/images/happy_little_elf-round.png" width="120" height="120"></center>
                """)

    with gr.Row():
        with gr.Column(scale=4):
            # 创建一个聊天机器人对象
            chatbot = gr.Chatbot(height=350, show_copy_button=True)
            # 创建一个文本框组件，用于输入 prompt。
            # Q: 你是谁？
            # Q: 为什么有的时候情绪会突然低落什么也不想做？
            # Q: 忍受了不少委屈，导致现在很敏感，易愤怒该如何调整？
            # Q: 什么是InternLM？
            # Q：去北京有哪些好玩的地方呢？
            msg = gr.Textbox(label="Prompt/问题")

            with gr.Row():
                # 创建提交按钮。
                chat_btn = gr.Button("Chat")
            with gr.Row():
                # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                clear = gr.ClearButton(
                    components=[chatbot], value="Clear console")
                
        # 设置按钮的点击事件。当点击时，调用上面定义的 direct_answer 函数，并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
        chat_btn.click(model_center.direct_answer, 
                            inputs=[msg, chatbot], 
                            outputs=[msg, chatbot])

    gr.Markdown("""提醒：<br>
    1. 初始化数据库时间可能较长，请耐心等待。
    2. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。
    3. 心理互助问答，非心理咨询，仅为心理知识分享。
    4. 数据来源于壹心理清洗，壹心理已过滤任何发布者信息部分，仅使用文本。
    5. 因提问者信息有限，回答为模糊匹配，并非适合每个人，仅供参考。 
    6. Github(喜欢的话欢迎star): https://github.com/jayjayhust/HappyElf_MentalCompanion <br>
    """)
gr.close_all()

# 直接启动
demo.launch()
