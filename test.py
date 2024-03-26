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
# print(qa_chain)
# question = "为什么说泰瑞莎修女很有智慧？"
# #answer,chat_history = qa_chain.answer(question)
# answer = qa_chain.answer(question)
# print(answer)
# question = "吸引力定律是什么？泰瑞莎修女是怎样应用它的"
# answer,chat_history = qa_chain.answer(question)
# print(answer)
# chat_history = qa_chain.clear_history()
# print(chat_history)
def ask_question(question, chat_history):
    """
    提出问题并获取答案的函数，同时管理历史记录长度。

    参数:
    - question: 提出的问题。
    - chat_history: 之前的问答对，格式为字符串列表。

    返回:
    - 新的聊天历史记录和最新的回答。
    """
    # 将字符串格式的历史记录转换回列表
    chat_history = eval(chat_history) if chat_history else []
    
    # 确保历史记录不超过20条
    if len(chat_history) > 20:
        chat_history = chat_history[-20:]
    
    # 调用问答链获取答案
    chat_history = qa_chain.answer(question)
    
    # 获取最后一次对话的答案
    _, latest_answer = chat_history[-1]
    
    return str(chat_history), latest_answer

# 设置 Gradio 界面
iface = gr.Interface(
    fn=ask_question,
    inputs=[gr.Textbox(label="Your question"), gr.Textbox(label="Chat History", value="[]")],
    outputs=[gr.Textbox(label="Updated Chat History"), gr.Textbox(label="Answer")],
    title="Chat Q&A with History",
    description="A chat interface with a history of Q&A. History is limited to the last 20 interactions."
)

# 启动 Gradio 应用
iface.launch()