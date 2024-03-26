# 首先导入所需第三方库
import uuid
from tqdm import tqdm
import os
import zhipuai
import gradio as gr
from tempfile import NamedTemporaryFile
import shutil
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from embedding.call_embedding import get_embedding
os.environ['ZHIPUAI_API_KEY'] = 'b441f069335a92a7f8679736ec1be3b9.1pnH2AoIw04JHMV1'
zhipuai.api_key = os.environ['ZHIPUAI_API_KEY']
DEFAULT_DB_PATH= "database/subtitles"
DEFAULT_PERSIST_PATH="data_base/vector_db"

def create_db_info(files=DEFAULT_DB_PATH, embeddings="zhipuai", persist_directory=DEFAULT_PERSIST_PATH):
    vectordb = create_db(files, persist_directory, embeddings)
    return ""
# 获取文件路径函数
def get_files(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            file_type = filename.split('.')[-1]
            if file_type == 'txt':
                file_list.append(os.path.join(filepath, filename))
    return file_list

# 加载文件函数
def get_text(dir_path):
    # args：dir_path，目标文件夹路径
    # 首先调用上文定义的函数得到目标文件路径列表
    file_lst = get_files(dir_path)
    # docs 存放加载之后的纯文本对象
    docs = []
    # 遍历所有目标文件
    for one_file in tqdm(file_lst):
        file_type = one_file.split('.')[-1]
        if file_type == 'txt':
            loader = UnstructuredFileLoader(one_file)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue
        docs.extend(loader.load())
    return docs

def create_db_info(files, embeddings="zhipuai", persist_directory=DEFAULT_PERSIST_PATH):
    if files is None:
        return "未上传文件", 

    # 创建一个临时文件列表存放上传的文件路径
    temp_files = []
    for file_info in files:
     if 'name' in file_info and 'file' in file_info:
        # 创建一个临时文件
        temp_file = NamedTemporaryFile(delete=False, suffix=file_info["name"])
        # 将上传的文件内容写入临时文件
        shutil.copyfileobj(file_info["file"], temp_file)
        # 关闭文件以确保写入完成
        temp_file.close()
        # 添加临时文件路径到列表
        temp_files.append(temp_file.name)

    # 调用原有的create_db函数，现在传递临时文件路径列表
    vectordb = create_db(temp_files, persist_directory, embeddings)

    # 清理临时文件
    for temp_file in temp_files:
        os.unlink(temp_file)

    return "向量化完成",

def create_db(files, persist_directory=DEFAULT_PERSIST_PATH, embeddings="zhipuai"):
# 加载目标文件
    docs = []
    for file_path in files:
        doc = get_text(file_path)
        if doc:  # 确保doc不为空
            docs.append(doc)

    # 对文本进行分块
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    if type(embeddings) == str:
        embeddings = get_embedding(embedding=embeddings)

    ids = [str(uuid.uuid4()) for _ in split_docs]

    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings, 
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )
    vectordb.persist()
    return vectordb

def presit_knowledge_db(vectordb):
    """
    该函数用于持久化向量数据库。

    参数:
    vectordb: 要持久化的向量数据库。
    """
    vectordb.persist()


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
