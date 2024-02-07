# HappyElf_MentalCompanion

## 书生·浦语大模型实战营大作业介绍
- 可以在班级群中随机组队完成一个大作业项目，一些可提供的选题如下：
  - 人情世故大模型：一个帮助用户撰写新年祝福文案的人情事故大模型
  - 中小学数学大模型：一个拥有一定数学解题能力的大模型
  - 心理大模型：一个治愈的心理大模型
  - 工具调用类项目：结合 Lagent 构建数据集训练 InternLM 模型，支持对 MMYOLO 等工具的调用
- 其他基于书生·浦语工具链的小项目都在范围内，欢迎大家充分发挥想象力。

## 选题（组队3~5人）
- 项目名称：快乐小精灵（HappyElf MentalCompanion）
- 项目简介：设计一款针对6-12岁小学阶段的情绪认知对话机器人，用故事化叙事的方式对小朋友的疑问进行引导和解答。
- 项目目标：选择一个垂直领域，收集该领域的专业资料构建专业知识库，并搭建专业问答助手，并在 OpenXLab 上成功部署。
- 实施路径：
  - 数据集处理
    - 数据集申请
    - 数据集分隔：将数据集划分为训练集（train）、验证集（开发集dev）、测试集（test）
    - 数据集清洗：
      - 训练数据集：
        - PsyQA_example.json处理：dataset_sample_clean.py
        - large_span_enstra_PsyQA_train_1.json：dataset_original_1_clean.py
        - large_span_enstra_PsyQA_train_2.json：dataset_original_2_clean.py
      - 测试数据集：
        - large_span_enstra_PsyQA_dev.json处理：dataset_original_dev.py
      - 验证数据集：
        - large_span_enstra_PsyQA_test.json处理：dataset_original_test.py
    - 数据集向量化并持久化：dataset_vectorization.py
  - 构建环境(https://blog.51cto.com/u_12870633/5950545)：
    - 软件环境：Ubuntu 20.04 + Anaconda + CUDA(11.7)/CUDNN(8.6.0) + pytorch 2.0.1
    - 硬件环境
      - InternStudio：https://studio.intern-ai.org.cn/console/instance
      - OpenXLab上申请：≥ 24GB nvidia显卡
  - 模型下载
    - 下载向量词模型sentence-transformer(还要配置NLTK相关资源)：hf_download_sentence-transformer.py，https://github.com/InternLM/tutorial/blob/main/langchain/readme.md#13-langchain-%E7%9B%B8%E5%85%B3%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE
    - 下载大模型InternLM2-Chat-7B大模型：modelscope_download_InternLM2-Chat-7B_run.py，https://modelscope.cn/models/Shanghai_AI_Laboratory/internlm2-chat-7b/summary
      - 大模型回答内容不断重复：注意设置repetition_penalty(设置高一点，比如1.1)
      - 爆显存的处理：
        - 降低batch_size
        - 降低max_seq_length
        - workspace里面config.ini 里面有cache_max_entry_count(表示k/v cache占 total mem的比例)，默认0.5，可以调到0.2
  - XTuner微调
    - 下载并安装最新版XTuner(https://github.com/InternLM/tutorial/blob/main/xtuner/README.md)：https://github.com/InternLM/xtuner
    - 用XTuner微调InternLM2-Chat-7B大模型：https://github.com/InternLM/tutorial/blob/main/xtuner/README.md#235-%E5%BC%80%E5%A7%8B%E5%BE%AE%E8%B0%83
    - 微调后的模型保存（PTH格式）：微调得到的 PTH 模型文件和其他杂七杂八的文件都默认在当前的 ./work_dirs 中
    - 模型转换：
      - PTH 模型转换为 HuggingFace 模型，即：生成 Adapter 文件夹（README.md，adapter_config.json，adapter_model.bin，xtuner_config.py等）。可以简单理解：LoRA 模型文件 = Adapter。
  - 微调后的模型部署
    - 部署到OpenXLab
      - 将微调后的模型存放至OpenXLab的模型中心进行托管：
        - 上传模型：https://openxlab.org.cn/docs/models/%E4%B8%8A%E4%BC%A0%E6%A8%A1%E5%9E%8B.html
        - 下载模型：https://openxlab.org.cn/docs/models/%E4%B8%8B%E8%BD%BD%E6%A8%A1%E5%9E%8B.html
      - 完成向量话并进行持久化的数据集存放在到github目录下（临时做法，后续考虑把数据集也托管到OpenXLab的数据集中心）
      - OpenXLab部署应用并启动
    - 部署到自己的GPU服务器
      - 用最新版LMDeploy(0.2.1适配最新的internlm2)部署到自己的GPU服务器：https://zhuanlan.zhihu.com/p/678920627?utm_psn=1734163474941394944
- 数据集及实现思路参考：
  - 心理大模型：一个治愈的心理大模型
    - 心理健康数据集：
      - PsyQA（一个中文心理健康问答数据集，完整数据集需申请。22K questions）：https://github.com/thu-coai/PsyQA
      - 中文心理健康支持对话数据集(SmileChat)与大模型(MeChat)：https://github.com/qiuhuachuan/smile
      - 心理数据集1(172条问答数据，英文)：https://huggingface.co/datasets/heliosbrahma/mental_health_chatbot_dataset
      - 心理数据集2(Collection of 33 Psychology Related Datasets)：https://www.kaggle.com/discussions/general/304994
      - 情感常用数据集整理：https://blog.csdn.net/weixin_43765589/article/details/132319745
      - SST 斯坦福情绪树库数据集：https://hyper.ai/datasets/15977（https://nlp.stanford.edu/sentiment/index.html）
      - 中文微博情感分析数据集（NLPCC2014）：https://hyper.ai/datasets/14390
      - ExpW 表情识别数据集：https://hyper.ai/datasets/17382
    - 参考文献：
      - 近期大模型动态：LLaMA-2-7B-32K的训练数据组织情况及面向儿童心理健康领域的微调模型推介：https://mp.weixin.qq.com/s/2_T0VKB_80UmZvW9VqrizQ
      - Falcon-7B大型语言模型在心理健康对话数据集上使用QLoRA进行微调：https://mp.weixin.qq.com/s/Pp1ra5zKn4CEQmrKOkBcjA
      - 人类的悲欢虽不相通，但情感分析模型读得懂：https://hyper.ai/news/14399
      - 心理学开放数据资源汇总 | 心理与行为大数据比赛数据源推荐：https://mp.weixin.qq.com/s/9eCAnjB8tM7ailrxXeCD2A
      - 大模型遇上心理健康咨询：MeChat、QiaoBan、SoulChat、MindChat四大心理健康领域微调模型总结：https://mp.weixin.qq.com/s/vSaHDJ6DxHVREefX8GHp_A
      - 基于百度文心一言ERNIE大模型的中文情感分析实战（自定义数据集）：https://mp.weixin.qq.com/s/oAGo3HMqxbaL4pY1p7qFGg
    - OpenXLab部署：
      - 应用部署：https://openxlab.org.cn/apps
      - 服务器资源申请（GPU，用于应用部署）：https://openxlab.org.cn/docs/apps/%E5%BA%94%E7%94%A8%E5%88%9B%E5%BB%BA%E6%B5%81%E7%A8%8B.html#%E8%B5%84%E6%BA%90%E7%94%B3%E8%AF%B7%E6%B5%81%E7%A8%8B
        - 配置1(8vCPU, 32GB内存, Nvidia A10 24GB)：python=3.9 gradio=3.18.0 cuda=11.7 torch=2.0.1
      - 注意事项：
        - 1.应用默认的启动文件为关联代码仓库根目录下的 app.py 文件 app.py 示例
        - 2.配置应用所需的运行环境，如有 Python 依赖项（pip 安装）可写入 requirements.txt 中，Debian 依赖项（apt-get 安装）可写入 packages.txt 中，并存放至代码仓库的根目录下
        - 3.如需提高应用中模型文件下载速度，建议尝试 模型托管
        - 4.应用默认在 7860 端口启动，请不要占用或改写个人应用的启动端口
      - 部署思路：
        - 先申请开通应用部署服务器
        - 再进入应用部署服务器，使用关联的github中的脚本，下载模型到本地（比如L3_sentence-transformer_download.py等）
        - 安装pip依赖包（pip install -r requirements.txt）
        - 加载向量数据库并持久化
        - 最后，在本地运行app.py文件，即可部署应用

## 项目参考
  - 食神：https://zhuanlan.zhihu.com/p/677682573
    - github：https://github.com/zhanghui-china/TheGodOfCookery
    - 数据集：
    ```json
    {
      "conversation": [{
        "system": "你是一个专业的厨师，你会做很多菜。用户报上自己所需的菜名后，你可以把做菜所需要的原料，以及做菜的方法告诉用户",
        "input": "软中带脆的干锅花菜的做法",
        "output": "您需要准备以下食材:\n['适量五花肉', '1颗花菜', '适量食用油', '1勺生抽', '适量葱花蒜片', '半勺蚝油', '适量盐']\n按以下方法制作:\n['一、准备\\n\\n1…菜花掰好切小头，泡盐水30分钟。\\n     再次用清水洗净，捞出控干\\n\\n2…五花肉洗净，切片，备用。\\n\\n3…切 葱花蒜片，备用。\\n\\n3…调汁：1勺生抽+半勺蚝油+适量盐\\n\\n', '二、炒\\n\\n1…热锅凉油，下葱花蒜片爆锅。\\n\\n2…下五花肉煸炒至变色后盛出\\n\\n3…用锅里剩下的油，下花菜煸炒。\\n\\n重点来了：\\n4…下花菜不停的翻炒，感觉温度逐渐升高\\n      到了如果不加水锅就要糊了的时候\\n      倒入一个碗底的清水，翻炒后盖上锅盖\\n      锅盖被水蒸气烀住了\\n      焖一小会，清水快收干的时候开锅盖\\n      （掌握时间，别弄糊了哈）\\n\\n5…此时花菜已经偏软了，下调好的汁\\n     翻炒没有汤汁为止，出锅', '花菜的脆梗，软蔫的花菜头太好吃了 ']"
      }]
    }
    ```
  - 心理健康大模型：EmoLLM
    - github：https://github.com/aJupyter/EmoLLM
  - Mentalhealth-心理健康大模型
    - https://github.com/xiexiaoshinick/Mental_Health_Support_Chatbot
