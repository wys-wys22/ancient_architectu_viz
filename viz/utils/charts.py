from pyecharts.charts import Pie, Bar, Line, Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType

def create_type_pie_chart(df):
    type_counts = df['type'].value_counts()
    data_pair = [(k, int(v)) for k, v in type_counts.items()]
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="400px"))
        .add(series_name="建筑类型", data_pair=data_pair, radius=["40%", "70%"],
             label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        .set_global_opts(title_opts=opts.TitleOpts(title="建筑类型比例", pos_left="center"))
        .set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} 座 ({d}%)"))
    )
    return pie.render_embed()

def create_era_line_chart(df):
    era_order = ['汉', '三国', '隋', '唐', '辽', '宋', '金', '元', '明', '清', '民国']
    era_counts = df['era'].value_counts()
    sorted_eras = [e for e in era_order if e in era_counts.index]
    counts = [era_counts[e] for e in sorted_eras]
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="400px"))
        .add_xaxis(sorted_eras)
        .add_yaxis("建筑数量", counts, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=3))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="建筑数量年代演变", pos_left="center"),
            xaxis_opts=opts.AxisOpts(name="朝代"),
            yaxis_opts=opts.AxisOpts(name="数量"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
        )
    )
    return line.render_embed()

def create_height_bar_chart(df):
    top10 = df.nlargest(10, 'height')[['name', 'height']]
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="400px"))
        .add_xaxis(top10['name'].tolist())
        .add_yaxis("高度（米）", top10['height'].tolist(), label_opts=opts.LabelOpts(position="top"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="建筑高度 Top10", pos_left="center"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
            yaxis_opts=opts.AxisOpts(name="高度 (m)"),
        )
    )
    return bar.render_embed()

def create_map_chart(df):
    """散点地图：建筑分布（城市聚合）"""
    city_counts = df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
    data_pairs = [(row['city'], int(row['count'])) for _, row in city_counts.iterrows()]
    geo = (
        Geo(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="100%", height="500px"))
        .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(border_color="#111"))
        .add("建筑密度", data_pairs, type_="effectScatter", symbol_size=12)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="古建筑地理分布（城市热力）", pos_left="center"),
            visualmap_opts=opts.VisualMapOpts(min_=1, max_=5, is_piecewise=False),
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} 处"),
        )
    )
    return geo.render_embed()