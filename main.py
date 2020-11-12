import time
import numpy as np
#import tensorflow as tf
import re
import string


with open('movie_lines.txt','r',encoding='utf-8',errors='ignore') as file:
	lines=file.read().split('\n')


with open('movie_conversations.txt','r',encoding='utf-8',errors='ignore') as file:
	conversations=file.read().split('\n')




id2_lines={}
j=0
for line in lines:
	id2_lines[line.split(' +++$+++ ')[0]]=line.split(' +++$+++ ')[-1]

conversations_list=[]

for convos in conversations:

	convo_=convos.split(' +++$+++ ')[-1][1:-1]
	convo_=convo_.replace("'","").replace(' ','').split(',')
	conversations_list.append(convo_)
    
    
del conversations
del lines


questions=[]
answers=[]
for convo in conversations_list:
	for i in range(0,len(convo)-1):
		questions.append(id2_lines[convo[i]])
		answers.append(id2_lines[convo[i+1]])



def clean_text(text):
    
    text=text.lower()
    text=re.sub(r"i'm",'i am',text)
    text=re.sub(r"what's",'what is',text)
    text=re.sub(r"he's",'he is',text)
    text=re.sub(r"she's",'she is',text)
    text=re.sub(r"/'re",' are',text)
    text=re.sub(r"/'ve",' have',text)
    text=re.sub(r"/'ll",' will',text)
    text=re.sub(r"/'d",' would',text)
    text=re.sub(r"wont't",' will not',text)
    text=re.sub(r"can't",' cannot',text)
    text=re.sub(r"[;{}<>!@#$%?.,;:|^&*()-]","",text)
    text=re.sub(r"/'bout"," about",text)
    text=re.sub(r'"' ,"",text)
    
    return text



questions_cleaned=[]
for question in questions:
	questions_cleaned.append(clean_text(question))

answers_cleaned=[]
for answer in answers:
	answers_cleaned.append(clean_text(answer))

del questions
del answers


word_2_count={}
for question,answer in zip(questions_cleaned,answers_cleaned):
    for words in question.split():
        if words not in word_2_count:
            word_2_count[words]=1
        else:
            word_2_count[words]+=1
    for words in answer.split():
        if words not in word_2_count:
            word_2_count[words]=1
        else:
            word_2_count[words]+=1
            

            
answers_word_2_int={}
j=0
for words,count in word_2_count.items():
    if count>50:
        answers_word_2_int[words]=j
        j+=1
question_word_2_int=answers_word_2_int.copy()


#tokens 
tokens=["<PAD>","<OUT>","<SOS>","<EOS>"]

for token in tokens:
    question_word_2_int[token]=len(question_word_2_int)+1
for token in tokens:
    answers_word_2_int[token]=len(answers_word_2_int)+1
    
    
int_word_answer={i:w for w,i in answers_word_2_int.items()}


for i in range(0,len(answers_cleaned)):
    answers_cleaned[i]+=" <EOS>"
    


questions_into_int=[]

for question in questions_cleaned:
    ints=[]
    for words in question.split():
        if words not in question_word_2_int:
            ints.append(question_word_2_int['<OUT>'])
        else:
            ints.append(question_word_2_int[words])
    questions_into_int.append(ints)
    
    
answers_into_int=[]
for answers in answers_cleaned:
    ints=[]
    for words in answers.split():
        if words not in answers_word_2_int:
            ints.append(answers_word_2_int['<OUT>'])
        else:
            ints.append(answers_word_2_int[words])
    answers_into_int.append(ints)
    


sorted_clean_questions=[]
sorted_clean_answers=[]

for i in range(1,26):
    for j,sentence in enumerate(questions_into_int):
        if len(sentence)==i:
            sorted_clean_questions.append(questions_into_int[j])
            sorted_clean_answers.append(answers_into_int[j])
            


        
    
    




            






