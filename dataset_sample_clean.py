# json数据加载：https://pythonjishu.com/ubrnbaxkgmxtyjb/

import json

file_path = './datasets/mental_health/original/PsyQA_example.json'  # 原始数据集
file_after_clean_path = './datasets/mental_health/PsyQA_example_cleaned.json'  # 输出的json文件数据集路径
file_after_clean_txt_path = './datasets/mental_health/PsyQA_example_cleaned.txt'  # 输出的txt文件数据集路径

with open(file_path, "r", encoding='utf-8') as f:
    content = f.read()
    data_json = json.loads(content)
    print('*' * 100)
    print(len(data_json))

    file_after_clean_txt = []
    pure_text = ""
    for record in data_json:
        txt_record = {}

        print('*' * 100)
        print(record)
        print('*' * 100)
        print(record['question'])  # 打印question字段
        txt_record['问题'] = record['question']
        pure_text = pure_text + '问题:' + record['question']
        print('*' * 100)
        print(record['answers'])
        if len(record['answers']) > 1:  # 多个回答
            i = 0
            for answer in record['answers']:
                print('*' * 100)
                print(answer['answer_text'])  # 打印answer字段
                if i == 0:
                    txt_record['答案'] = answer['answer_text']
                    pure_text = pure_text + "\n" + '回答:' + answer['answer_text'] + "\n\n"
                # 删除多余字段
                if answer.get("has_label") is not None:
                    del answer["has_label"]
                if answer.get("labels_sequence") is not None:
                    del answer["labels_sequence"]
                i += 1
        else:  # 单个回答
            answer = record['answers'][0]
            print('*' * 100)
            print(answer['answer_text'])  # 打印answer字段
            txt_record['答案'] = answer['answer_text']
            pure_text = pure_text + "\n" + '回答:' + answer['answer_text'] + "\n\n"
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

        file_after_clean_txt.append(txt_record)
    
    with open(file_after_clean_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        json.dump(data_json, f, ensure_ascii=False, indent=4)
        print("写入JSON文件完成...")
        f.close()
    
    with open(file_after_clean_txt_path, 'w', encoding='utf-8') as f: # ‘w’表示写入文件，文件不存在则创建，存在则覆盖
        # json.dump(file_after_clean_txt, f, ensure_ascii=False, indent=4)
        f.write(pure_text)
        print("写入TXT文件完成...")
        f.close()

