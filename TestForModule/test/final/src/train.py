# 模型训练脚本
# src/preprocess.py
import pandas as pd
from config import config

def load_data(file_path):
    return pd.read_csv(file_path)

def save_data(data, file_path):
    data.to_csv(file_path, index=False)
