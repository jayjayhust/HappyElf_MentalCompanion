# json数据加载：https://pythonjishu.com/ubrnbaxkgmxtyjb/

import json

file_path = './datasets/mental_health/original/full_PsyQA/PsyQA_generation_split/large_span_enstra_PsyQA_dev.json'  # 原始数据集
file_after_clean_path = './datasets/mental_health/large_span_enstra_PsyQA_dev_cleaned.json'  # 输出的json文件数据集路径
file_after_clean_txt_path = './datasets/mental_health/large_span_enstra_PsyQA_dev_cleaned.txt'  # 输出的txt文件数据集路径

with open(file_path, "r", encoding='utf-8') as f:
    content = f.read()
    data_json = json.loads(content)
    print('*' * 100)
    print(len(data_json))

    file_after_clean_txt = []
    pure_text = ""
    for record in data_json:
        # record形如：
        # '
        # [QUESTION]中职高三，宿舍关系一直让我难以想象？
        # [DESCRIPTION]中职高三（考试也难，学科也不简单）的我，早已接受了学生素质差，但是自高二换宿舍以后开始宿舍关系一直让我难以想象，部分人晚上不睡觉，叨叨没完，早上又起不来。说话引起民愤也只是暂时有用。本来就敏感的我有声音就睡不着，我也只能在忍不了的时候提醒，提醒不管用，就得吵（骂），关系差是绝对的，我们宿舍其他舍友和舍友之间也有矛盾，一个喜欢吹牛，另一个舍友也是他好朋友，就和他闹掰了。宿舍里面俩人不说话正常不过了。这几个人有一个共同特点，自私。周末因为值日问题，能满地泡面袋，垃圾袋没人管。为啥就我宿舍这个样子，为啥我看见他们就恶心（是真的反胃），现在天天掉头发，大把大把掉。也许少量的字说明不了啥，但是我自从进入这个宿舍一来，一直都在提防每一个人。
        # [LABEL]人际,矛盾冲突,舍友同学,人际边界
        # [ANSWER][SUP]你好~~~给您一个温暖的抱抱，从您的描述中我了解到了您正在面临比较恶劣的宿舍舍友关系的问题，对此，我有以下的一些建议希望可以帮到您首先，从您的描述中可以看出，宿舍里的矛盾不仅仅限于您和其他舍友之间，其他舍友彼此间也存在矛盾，我想，这样的关系不仅仅对您造成了负面影响，对于其他舍友而言也一定有所影响，因此，我们不妨尝试着让大家一起好好沟通一下，看是否能制定一个彼此都认同的“宿舍规则”，让每个人都从规则中“获益”，这样也能增加彼此遵守规则的可能性另一方面，我们是否可以尝试着和老师沟通、汇报宿舍存在的问题呢？[ADV]如果舍友间沟通的确没有太大作用，我们可以试着和父母、老师等负责人沟通，表示希望换一间宿舍或是寻找别的住宿。
        # '
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

