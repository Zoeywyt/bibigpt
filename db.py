# 首先导入所需第三方库
from tqdm import tqdm
import os
import zhipuai
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from embedding.zhipuai_embedding import ZhipuAIEmbeddings
os.environ['ZHIPUAI_API_KEY'] = 'b441f069335a92a7f8679736ec1be3b9.1pnH2AoIw04JHMV1'
zhipuai.api_key = os.environ['ZHIPUAI_API_KEY']
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

# 目标文件夹
tar_dir = [
"C:/Users/zoey/Desktop/bibi/bibi/database/subtitles"
]

# 加载目标文件
docs = []
for dir_path in tar_dir:
    docs.extend(get_text(dir_path))

# 对文本进行分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=150)
split_docs = text_splitter.split_documents(docs)


embedding = ZhipuAIEmbeddings()
# 加载开源词向量模型
# embeddings = HuggingFaceEmbeddings(model_name="/root/data/model/sentence-transformer")
# 定义一个函数来获取文本的嵌入向量
def get_zhipu_embedding(text):
    return embedding.embed_query(text)
# 构建向量数据库
# 定义持久化路径
persist_directory = 'data_base/vector_db/chroma'
# 加载数据库
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding, 
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)
# 将加载的向量数据库持久化到磁盘上
vectordb.persist()