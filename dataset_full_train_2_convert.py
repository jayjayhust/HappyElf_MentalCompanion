# json数据加载：https://pythonjishu.com/ubrnbaxkgmxtyjb/

import json

file_train_2_path = './datasets/mental_health/PsyQA_full_train_2.json'  # 训练数据集1路径（10000条数据）
file_train_2_converted_path = './datasets/mental_health/PsyQA_full_train_2_converted.json'  # 

def dataset_convert(file_path, file_converted_path):
    file_dev_converted = []  # 调试数据集转换后的数据

    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        data_json = json.loads(content)
        print('*' * 100)
        print("数据集大小:", len(data_json))  # 22341条数据

        for i, record in enumerate(data_json):
            if len(record['answers']) > 1:  # 多个回答
                for answer in record['answers']:
                    # 删除多余字段
                    if "has_label" in answer:
                        del answer["has_label"]
                    if "labels_sequence" in answer:
                        del answer["labels_sequence"]
            else:  # 单个回答
                answer = record['answers'][0]
                # 删除多余字段
                if "has_label" in answer:
                    del answer["has_label"]
                if "labels_sequence" in answer:
                    del answer["labels_sequence"]
            # 删除多余字段
            if "description" in record:
                del record["description"]
            if "questionID"  in record:
                del record["questionID"]
            if "keywords"  in record:
                del record["keywords"]
            
            record['instruction'] = "现在你扮演一位专业的心理咨询师，你具备丰富的心理学和心理健康知识。" + \
            "你擅长运用多种心理咨询技巧，例如认知行为疗法原则、动机访谈技巧和解决问题导向的短期疗法。" + \
            "以温暖亲切的语气，展现出共情和对来访者感受的深刻理解。以自然的方式与来访者进行对话，" + \
            "避免过长或过短的回应，确保回应流畅且类似人类的对话。提供深层次的指导和洞察，" + \
            "使用具体的心理概念和例子帮助来访者更深入地探索思想和感受。避免教导式的回应，" + \
            "更注重共情和尊重来访者的感受。根据来访者的反馈调整回应，确保回应贴合来访者的情境和需求。请为以下的对话生成一个回复。" + \
            "\n\n对话：\n来访者：{}。".format(record['question']) + \
            "\n咨询师："
            record['output'] = record['answers'][0]['answer_text']
            # # 创建一个映射，将旧键映射到新键
            # key_map = {'question': 'query', 'answers': 'outputs', 'answer_text': 'text'}
            # # 遍历原有键，并替换为新键
            # new_data = {key_map.get(k, k): v for k, v in record.items()}
            del record["question"]
            del record["answers"]
            file_dev_converted.append(record)
            pass

        with open(file_converted_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
            json.dump(file_dev_converted, f, ensure_ascii=False, indent=4)
            print("写入JSON文件完成...")
            f.close()

if __name__ == '__main__':
    dataset_convert(file_train_2_path, file_train_2_converted_path)