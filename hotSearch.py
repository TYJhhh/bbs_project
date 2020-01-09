import requests
import re
import bs4
from pyecharts.charts import Bar


# 获取HTML文本
def getHTMLText(url):
    try:
        # 模拟浏览器
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("InternetError!")
        return " "

# 解析并且返回HTML文本
def HTMLTextconvert(html):
    try:
        soup = bs4.BeautifulSoup(html, "html.parser")
        return soup
    except:
        print("HTMLConvertError!")
        return " "

# 检索HTML中的信息，获取搜索排名信息
# 存在置顶的情况，需要特殊判断
def HTMLSearch(html, ranklist):
    try:
        flag = 0
        # 找到所有tbody标签下的所有内容，并且遍历所有的儿子节点
        for tr in html.find("tbody").children:
            # 添加判断：获得的内容是否为标签Tag类型
            if isinstance(tr, bs4.element.Tag):
                # 使用flag特判置顶的情况
                if flag == 0:
                    rank = "置顶"
                    # 注意由于class属性会和python中的关键字重名，因此需要变为class_
                    td02 = tr.find_all(class_=re.compile('td-02'))
                    for i in td02:
                        if isinstance(i, bs4.element.Tag):
                            # trans得到的类型为列表
                            trans = i.find_all("a")
                    number = " "
                    ranklist.append([rank, trans[0].string, number])
                    flag = 1
                else:
                    # 排名信息在td标签下的class=td-01属性中
                    td01 = tr.find_all(class_=re.compile("td-01"))
                    for i in td01:
                        if isinstance(i, bs4.element.Tag):
                            rank = i.string
                    # 热搜内容和搜索量在td标签下的class=td-02属性中：内容是a标签，搜索量是span标签
                    td02 = tr.find_all(class_=re.compile("td-02"))
                    for i in td02:
                        name = i.find_all("a")
                        column = i.find_all("span")


                    result = []
                    # 查找文档中所有a标签
                    for k in tr.find_all('a'):
                        link = k.get('href')
                        link1 = k.get('href_to')
                        # 过滤没找到的
                        if (link is not None):
                            # 过滤非法链接
                            if link == '#':
                                pass
                            if link == 'javascript:void(0);':
                                result.append(link1)
                            else:
                                result.append(link)
                    # print(result)
                    # print(name)
                    # 使用string获取字符串信息不准确，因为微博还有一些热搜标题为含有表情的，因此使用了text
                    ranklist.append([rank, name[0].text, column[0].text,result[0]])
    except:
        print("HTMLSearchError!")

def RankHTML(ranklist):
    # 将搜索结果热度进行排序 取前10个热搜
    data = []
    for i in range(1,10):
        data.append(ranklist[i][2])
    cities = []
    for i in range(1, 10):
        ranklist[i][1] = (ranklist[i][1])[0:2]
        cities.append(ranklist[i][1])
    # 然后将其放入pyecharts中展示
    bar = Bar()
    bar.add_xaxis(cities)
    bar.add_yaxis("热搜排行", data)
    bar.render('hot.html')

# 主函数
def main():
    try:
        # 微博热搜的网站
        url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
        # 使用二维列表存储每一条热搜信息的rank信息和内容
        rank = []
        text = getHTMLText(url)
        soup = HTMLTextconvert(text)
        HTMLSearch(soup, rank)

        #RankHTML(rank)

    except:
        print("SystemError!")
        return 0
    return rank
#main()