# json数据加载：https://pythonjishu.com/ubrnbaxkgmxtyjb/

import json

file_path = './datasets/mental_health/original/full_PsyQA/PsyQA_full.json'  # 原始数据集（22341条数据）
file_train_1_path = './datasets/mental_health/PsyQA_full_train_1.json'  # 训练数据集1路径（10000条数据）
file_train_2_path = './datasets/mental_health/PsyQA_full_train_2.json'  # 训练数据集2路径（10000条数据）
file_dev_path = './datasets/mental_health/PsyQA_full_train_dev.json'  # 验证数据集路径（1150条数据）
file_test_path = './datasets/mental_health/PsyQA_full_test.json'  # 测试数据集路径（1191条数据）


with open(file_path, "r", encoding='utf-8') as f:
    content = f.read()
    data_json = json.loads(content)
    print('*' * 100)
    print(len(data_json))  # 22341条数据

    for i, record in enumerate(data_json):
        if len(record['answers']) > 1:  # 多个回答
            for answer in record['answers']:
                # 删除多余字段
                if answer.get("has_label") is not None:
                    del answer["has_label"]
                if answer.get("labels_sequence") is not None:
                    del answer["labels_sequence"]
        else:  # 单个回答
            answer = record['answers'][0]
            # 删除多余字段
            if answer.get("has_label") is not None:
                del answer["has_label"]
            if answer.get("labels_sequence") is not None:
                del answer["labels_sequence"]
        # 删除多余字段
        if record.get("description") is not None:
            del record["description"]
        if record.get("questionID") is not None:
            del record["questionID"]
    
    with open(file_train_1_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        json.dump(data_json, f, ensure_ascii=False, indent=4)
        print("写入JSON文件完成...")
        f.close()

