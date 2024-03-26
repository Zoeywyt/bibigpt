import sys 
sys.path.append("../embedding") 
sys.path.append("../database") 
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings    # 调用 OpenAI 的 Embeddings 模型
import os
from embedding.zhipuai_embedding import ZhipuAIEmbeddings

# from create_db import create_db,load_knowledge_db
from embedding.call_embedding import get_embedding

def get_vectordb(file_path:str=None, persist_path:str=None, embedding = "openai",embedding_key:str=None):
    """
    返回向量数据库对象
    输入参数：
    question：
    llm:
    vectordb:向量数据库(必要参数),一个对象
    template：提示模版（可选参数）可以自己设计一个提示模版，也有默认使用的
    embedding：可以使用zhipuai等embedding，不输入该参数则默认使用 openai embedding，注意此时api_key不要输错
    """
    embedding = get_embedding(embedding=embedding, embedding_key=embedding_key)
    if os.path.exists(persist_path):  #持久化目录存在
        vectordb = load_knowledge_db(persist_path, embedding)

    return vectordb
def load_knowledge_db(path, embeddings):
    """
    该函数用于加载向量数据库。

    参数:
    path: 要加载的向量数据库路径。
    embeddings: 向量数据库使用的 embedding 模型。

    返回:
    vectordb: 加载的数据库。
    """
    vectordb = Chroma(
        persist_directory=path,
        embedding_function=embeddings
    )
    return vectordb