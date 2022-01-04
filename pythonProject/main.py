import os
from datetime import date
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Page, Scatter, Boxplot, WordCloud
from pyecharts.globals import ThemeType

# 数据爬取
def spider():
    def get_page(url):
        # 获取响应头
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        # 验证是否爬取成果
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.json()

        except Exception as e:
            print("Error", e)
            return ""

    # 解析html网页代码
    def parse_page(data_json):
        data = data_json['data']['list']
        date = data_json['data']['cachetime'].split(' ')[0]
        all_data = []
        for i in data:
            if len(i['city']) != 0:
                province = i['name']
                for j in i['city']:
                    data_one = {}
                    # 省份
                    data_one['province'] = province
                    # 城市
                    data_one['city'] = j['name']
                    # 确诊人数
                    data_one['sureNum'] = j['conNum']
                    # 治愈人数
                    data_one['cureNum'] = j['cureNum']
                    # 死亡人数
                    data_one['deathNum'] = j['deathNum']
                    # 日期
                    data_one['date'] = date
                    all_data.append(data_one)
            else:
                # 台湾、香港、澳门城市为空，需要单独追加
                data_one = {}
                data_one['province'] = i['name']
                data_one['city'] = i['name']
                data_one['sureNum'] = i['value']
                data_one['deathNum'] = i['deathNum']
                data_one['cureNum'] = i['cureNum']
                data_one['date'] = date
                all_data.append(data_one)
        result = pd.DataFrame(all_data)
        print(result)
        return (result)

    # 保存数据
    def save_file(data_df):
        columns = ['province', 'city', 'sureNum', 'deathNum', 'cureNum', 'date']
        if os.path.exists('疫情数据.xlsx'):
            data_df.to_excel('疫情数据.xlsx',
                             mode='a',
                             columns=columns,
                             encoding='utf-8',
                             header=False,
                             index=False)
        else:
            data_df.to_excel('疫情数据.xlsx',
                             columns=columns,
                             encoding='utf-8',
                             index=False)

    if __name__ == "__main__":
        url = 'https://gwpre.sina.cn/interface/fymap2020_data.json?1582011487323'
        data_json = get_page(url)
        result = parse_page(data_json)
        if os.path.exists('疫情数据.xlsx'):
            os.remove('疫情数据.xlsx')
        save_file(result)

# 绘制柱状图
def bar1_get():
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))
            # 设置x轴--疫情治愈地区的列表
            .add_xaxis(list(obj_sure.keys()))
            # 设置y轴--对应疫情地区治愈人数的列表
            .add_yaxis("治愈人数", list(obj_sure.values()), category_gap=0,
                       color="red", gap="100%")
            # 设置柱状图标题
            .set_global_opts(title_opts=opts.TitleOpts(title="全国新冠肺炎疫情累计治愈人数",
                                                       # 设置柱状图副标题
                                                       subtitle="更新时间：{}".format(date.today()),
                                                       # 设置柱状图标题位置制定
                                                       pos_top="top"))
            # 是否显示y轴的值
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                             )
    )

    return bar

def bar2_get():
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))
            # 设置x轴--疫情死亡地区的列表
            .add_xaxis(list(obj_sure.keys()))
            # 设置y轴--对应疫情地区死亡人数的列表
            .add_yaxis("死亡人数", list(obj_death.values()), category_gap=0,
                       color="blue", gap="100%")
            # 设置柱状图标
            .set_global_opts(title_opts=opts.TitleOpts(title="全国新冠肺炎疫情累计死亡人数",
                                                       # 设置柱状图副标题
                                                       subtitle="更新时间：{}".format(date.today()),
                                                       # 设置柱状图标题位置制定
                                                       pos_top="top"))
            # 是否显示y轴的值
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                             )
    )
    return bar

# 绘制饼图
def pie1_get():
    pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))
    # 拼接治愈地区列表和治愈人数列表，形成一个新列表，列表中的每一个元素都是一个元组
    data = list(zip(list(obj_death.keys()), list(obj_death.values())))
    # 为饼图添加data数据
    pie.add("治愈人数", data)
    # 设置标题
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="治愈人数"),
        # 将标题设置在右边
        legend_opts=opts.LegendOpts(pos_right="right")
    )
    # 饼图各部分所表示的城市，治愈人数，所占的百分比
    # pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}人:{d}%"))
    return pie

def pie2_get():
    pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))
    # 拼接死亡地区列表和死亡人数列表，形成一个新列表，列表中的每一个元素都是一个元组
    data = list(zip(list(obj_death.keys()), list(obj_death.values())))
    # 为饼图添加data数据
    pie.add("死亡人数", data)
    # 设置标题
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="死亡人数"),
        # 将标题设置在右边
        legend_opts=opts.LegendOpts(pos_right="right")
    )
    return pie

def cloud_get():
    url = "https://top.baidu.com/board?tab=realtime"
    list_title = []
    list_num = []
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
    }
    # 发送请求
    resp = requests.get(url, headers=headers)
    html = resp.content
    soup = BeautifulSoup(html, 'html.parser')
    hot_title = soup.find_all('span', class_="one-line-ellipsis _38vEKmzrdqNxu0Z5xPExcg")#c-single-text-ellipsis
    hot_number = soup.find_all('span', class_="_2-OsoCiQjnZhfC5xiIyFR3")#hot-index_1Bl1a
    for item in hot_title:
        list_title.append(item.get_text())
    for item in hot_number:
        list_num.append(int(item.get_text().replace("万", "0000")))
    data = {
        "title": list_title,
        "number": list_num,
    }
    df_data = DataFrame(data)
    columns = ['title', 'number']
    if os.path.exists('热搜数据.xlsx'):
        os.remove('热搜数据.xlsx')
    if os.path.exists('热搜数据.xlsx'):
        df_data.to_excel('热搜数据.xlsx',
                         mode='a',
                         columns=columns,
                         encoding='utf-8',
                         header=False,
                         index=False)
    else:
        df_data.to_excel('热搜数据.xlsx',
                         columns=columns,
                         encoding='utf-8',
                         index=False)
    df = pd.read_excel("热搜数据.xlsx")
    dfnum = df.loc[:]
    obj = {}
    for row in dfnum.iterrows():
        if row[1]['title'] not in obj.keys():
            obj[row[1]['title']] = row[1]['number']
    data_wc = list(zip(list(obj.keys()), list(obj.values())))
    print(data_wc)
    wc = (
       WordCloud(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))
            .add("",
                 data_wc,
                 word_size_range=[10, 80],
                 word_gap=5,
                 shape="circle")
            .set_global_opts(title_opts=opts.TitleOpts(title="全国疫情词云"))
    )
    return wc

def scatter_get():
    df_city = df.loc[:, ['province', 'city', 'sureNum']]

    df_city = df_city.drop(0)

    obj = {}

    for row in dfnum.iterrows():

        if row[1]['province'] not in obj.keys():
            obj[row[1]['province']] = []

        obj[row[1]['province']].append(row[1]['sureNum'])

    sc = (

        Scatter(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))

            .add_xaxis(list_cure)

            .add_yaxis("治愈人数", y_axis=list_num)

    )

    return sc

def box_get():
    df_city = df.loc[:, ['province', 'city', 'sureNum']]

    df_city = df_city.drop(0)

    obj = {}

    for row in dfnum.iterrows():

        if row[1]['province'] not in obj.keys():
            obj[row[1]['province']] = []

        obj[row[1]['province']].append(row[1]['sureNum'])

    list_box = list(obj.values())

    bp = Boxplot(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width="100%", height="800px"))

    bp.add_xaxis(list_cure)

    bp.add_yaxis("治愈人数", list_box)

    return bp

def page_simple():
    page = Page(layout=Page.DraggablePageLayout, )

    page.add(
        bar1_get(),
        bar2_get(),
        pie1_get(),
        pie2_get(),
        #scatter_get(),
        #box_get(),
        cloud_get()
    )
    page.render("demo.html")
    print("绘图完毕")


if __name__ == '__main__':
    spider()
    # 治愈人数
    obj_sure = {}
    # 死亡人数
    obj_death = {}
    # 读取爬虫生成的excel文件中的内容
    df = pd.read_excel("疫情数据.xlsx")
    # 按列读取excel表中的对应3列，存储格式为dataframe
    dfnum = df.loc[:, ['province', 'sureNum', 'deathNum']]
    # 遍历列
    for row in dfnum.iterrows():
        # 判断obj_sure中有无对应的建，如果没有设置键以及对应的值，如果有将对应地区的治愈人数累加
        if row[1]['province'] not in obj_sure.keys():
            obj_sure[row[1]['province']] = row[1]['sureNum']
        obj_sure[row[1]['province']] += row[1]['sureNum']
    # 遍历列
    for row in dfnum.iterrows():
        # 判断obj_death中有无对应的建，如果没有设置键以及对应的值，如果有将对应地区的死亡人数累加
        if row[1]['province'] not in obj_death.keys():
            obj_death[row[1]['province']] = row[1]['deathNum']
        obj_death[row[1]['province']] += row[1]['deathNum']
    list_cure = list(obj_sure.keys())
    list_num = list(obj_sure.values())
    page_simple()