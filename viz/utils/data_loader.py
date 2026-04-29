import pandas as pd
import os
from django.conf import settings

def load_data():
    """读取 buildings.csv 并返回 DataFrame"""
    csv_path = os.path.join(settings.BASE_DIR, 'data', 'buildings.csv')
    df = pd.read_csv(csv_path)
    # 确保数据类型
    df['height'] = pd.to_numeric(df['height'], errors='coerce')
    df['importance'] = pd.to_numeric(df['importance'], errors='coerce')
    return df

def get_type_stats(df):
    return df['type'].value_counts().to_dict()

def get_era_stats(df):
    return df['era'].value_counts().to_dict()