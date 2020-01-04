import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
ALL_DATA = []
def parse_page(url):
    response = requests.get(url, headers=headers) # 网络请求 返回结果
    text = response.content.decode('utf-8')
    # pip install html5lib html5
    soup = BeautifulSoup(text, 'html5lib')
    conMidtab = soup.find('div', class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city_list = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            temp_list = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({'city': city_list, 'temp_min': int(temp_list)})
            # print({'city': city_list, 'temp_min': int(temp_list)})

def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]

    for url in urls:
        parse_page(url)

    # 将结果按照最低气温进行排序 取前10个城市
    ALL_DATA.sort(key=lambda data: data['temp_min'])
    # print(ALL_DATA[0:10])
    data = ALL_DATA[0:10]
    cities = list(map(lambda x: x['city'], data))
    # print(cities)
    temp_min = list(map(lambda x: x['temp_min'], data))
    # 然后将其放入pyecharts中展示
    bar = Bar()
    bar.add_xaxis(cities)
    bar.add_yaxis("最低气温", temp_min)

    bar.render('temprater.html')

if __name__ == "__main__":
    main()