from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import os
from django.conf import settings


def load_data():
    """加载数据"""
    csv_path = os.path.join(settings.BASE_DIR, 'data', 'buildings.csv')
    print(f"加载数据: {csv_path}")

    if not os.path.exists(csv_path):
        print("❌ 数据文件不存在")
        return None

    df = pd.read_csv(csv_path)
    df['height'] = pd.to_numeric(df['height'], errors='coerce')
    return df


def index(request):
    """主页"""
    return render(request, 'viz/index.html')


def chart_data_api(request):
    """提供图表数据 API（含地图数据）"""
    df = load_data()

    if df is None:
        return JsonResponse({'error': '数据加载失败'}, status=500)

    # 1. 类型比例（饼图）
    type_counts = df['type'].value_counts()
    type_data = [{'name': k, 'value': int(v)} for k, v in type_counts.items()]

    # 2. 年代趋势（折线图）
    era_order = ['汉', '三国', '隋', '唐', '辽', '宋', '金', '元', '明', '清', '民国']
    era_counts = df['era'].value_counts()
    era_labels = [e for e in era_order if e in era_counts.index]
    era_values = [int(era_counts[e]) for e in era_labels]

    # 3. 高度 Top10（柱状图）
    top10 = df.nlargest(10, 'height')
    top10_names = top10['name'].tolist()
    top10_heights = [float(h) for h in top10['height'].tolist()]

    # 4. 热力地图数据（城市 + 建筑数量）
    city_counts = df['city'].value_counts()
    map_data = [{'name': city, 'value': int(count)} for city, count in city_counts.items()]

    return JsonResponse({
        'type_data': type_data,
        'era_labels': era_labels,
        'era_counts': era_values,
        'top10_names': top10_names,
        'top10_heights': top10_heights,
        'map_data': map_data,  # 地图数据
    })