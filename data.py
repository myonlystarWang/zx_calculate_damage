import pandas as pd
import os

# 用于保存留言数据的文件路径
comments_file_path = "./comments_data.csv"

def load_comments_data(file_path=None):
    file_path = file_path or comments_file_path
    try:
        comments_data = pd.read_csv(file_path)
    except FileNotFoundError:
        comments_data = pd.DataFrame(columns=["时间", "昵称", "联系方式", "留言", "回复"])
    return comments_data if not comments_data.empty else pd.DataFrame(columns=["时间", "昵称", "联系方式", "留言", "回复"])

def save_comments_data(comments_data, file_path=None):
    file_path = file_path or comments_file_path
    
    # 检查目录是否存在，不存在则创建
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    comments_data.to_csv(file_path, index=False)