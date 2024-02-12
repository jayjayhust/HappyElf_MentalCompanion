# json数据加载：https://pythonjishu.com/ubrnbaxkgmxtyjb/

import json

file_path = './datasets/mental_health/original/full_PsyQA/PsyQA_full.json'  # 原始数据集（22341条数据）

file_train_1_path = './datasets/mental_health/PsyQA_full_train_1.json'  # 训练数据集1路径（10000条数据）
file_train_2_path = './datasets/mental_health/PsyQA_full_train_2.json'  # 训练数据集2路径（10000条数据）
file_dev_path = './datasets/mental_health/PsyQA_full_dev.json'  # 验证数据集路径（1150条数据）
file_test_path = './datasets/mental_health/PsyQA_full_test.json'  # 测试数据集路径（1191条数据）

file_train_1 = []  # 训练数据集1
file_train_2 = []  # 训练数据集2
file_dev = []  # 验证数据集
file_test = []  # 测试数据集
with open(file_path, "r", encoding='utf-8') as f:
    content = f.read()
    data_json = json.loads(content)
    print('*' * 100)
    print(len(data_json))  # 22341条数据

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
        
        if i < 10000:  # 训练数据集1
            file_train_1.append(record)
        elif i < 20000:  # 训练数据集2
            file_train_2.append(record)
        elif i < 21150:  # 验证数据集
            file_dev.append(record)
        else:  # 测试数据集
            file_test.append(record)
        pass

    with open(file_train_1_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        json.dump(file_train_1, f, ensure_ascii=False, indent=4)
        print("写入train 1 JSON文件完成...")
        f.close()
    with open(file_train_2_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        json.dump(file_train_2, f, ensure_ascii=False, indent=4)
        print("写入train 1 JSON文件完成...")
        f.close()
    with open(file_dev_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        json.dump(file_dev, f, ensure_ascii=False, indent=4)
        print("写入dev JSON文件完成...")
        f.close()
    with open(file_test_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        json.dump(file_test, f, ensure_ascii=False, indent=4)
        print("写入test JSON文件完成...")
        f.close()

