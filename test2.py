import os
import zhipuai
import gradio as gr
from qa_chain.Chat_QA_chain_self import Chat_QA_chain_self #带历史记录的问答链
from qa_chain.QA_chain_self import QA_chain_self  
from dotenv import load_dotenv, find_dotenv
from typing import Any, Dict, Optional


    
model:str = "glm-4"
temperature:float=0.3
top_k:int=4 
chat_history:list=[] 
file_path:str = "C:/Users/zoey/Desktop/bibi/bibi/database/subtitles"
persist_path:str = "data_base/vector_db/chroma"
# appid:str=None 
api_key:str = zhipuai.api_key   #or 从本地环境读取
# api_secret:str=None 
embedding = "zhipuai"     # ["openai","zhipuai"]  默认openai
qa_chain = Chat_QA_chain_self(model=model, temperature=temperature, top_k=top_k, chat_history=chat_history, file_path=file_path, persist_path=persist_path,  embedding = embedding, )
print(qa_chain)
question = "为什么说泰瑞莎修女很有智慧？"
#answer,chat_history = qa_chain.answer(question)
answer = qa_chain.answer(question)
print(answer)
question = "吸引力定律是什么？泰瑞莎修女是怎样应用它的"
answer,chat_history = qa_chain.answer(question)
print(answer)
chat_history = qa_chain.clear_history()
print(chat_history)
