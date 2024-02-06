import json
import re
with open('PsyQA_full.json','r',encoding='utf-8') as f:
    json_data = json.load(f)

ldata = []
labels = []
stra2label = {'Others':0,'Approval and Reassurance':1,'Information':2,'Restatement':3,'Direct Guidance':4,'Interpretation':5,'Self-disclosure':6}

from sklearn.model_selection import train_test_split



def split_mid(text,label): # This is a very rough method to split, we believe there must be a better method.
    text_len = 0
    for ld in text:
        text_len+=len(ld)
    if text_len>460 and len(text)>=2:
        s1 = split_mid(text[:len(text)//2],label[:len(text)//2])
        s2 = split_mid(text[len(text)//2:],label[len(text)//2:])
        return s1[0]+s2[0],s1[1]+s2[1]
    else:
        return [text],[label]

ctx_data=[]
max_b = 0
for d in json_data:
    for ans in d['answers']:
        if ans['has_label']:
            ldata = []
            labels = []
            for seq in ans['labels_sequence']:
                start,end,stra=seq['start'],seq['end'],seq['type']
                tmp = ans['answer_text'][start:end]
                single_sents = re.split(r"([。？！…]+)",tmp)
                for i in range(0,len(single_sents)-1,2):
                    ldata.append(single_sents[i]+single_sents[i+1])
                    labels.append(stra2label[stra])
            
            text_len = 0
            a,b = split_mid(ldata,labels)
            if max_b<len(b):
                max_b = len(b)
            for x,y in zip(a,b):  
                ctx_data.append({'text':x,'label':y})

train, tmp = train_test_split(ctx_data, train_size = 0.8, random_state=42)
dev, test = train_test_split(tmp, train_size=0.5, random_state=42)

