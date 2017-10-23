from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
chengxu = client['chengxu']
url_list = chengxu['url_list']

# spider 1 爬取首页中显示的类目中，一个类目下的所有商品的链接
def get_links_from(channel,pages,who_sells=0): # who_sells = 0表示个人，1表示商家
    #http://bj.58.com/shouji/1/pn2/
    list_view = '{}{}/pn{}/'.format(channel,str(who_sells),str(pages)) # 找网页规律的时候，刚刷新和点击后的相同页面的网址会有变化，但页面相同，它们是等价的，所以找页面规律时要多点击或刷新来找
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('td','t'):  # 一个类目的页码是有限的，通过寻找td.t来判断系统是否爬过头了
        for link in soup.select('td.t  a.t'):  # 这里的td.t a.t 是点击某个分类后的新网页的每个具体商品的链接的selector
            # 注意!!!上面代码后面，若是('td.t >a.t')即无法显示结果，必须空格！这样才对('td.t > a.t')
            item_link = link.get('href').split('?')[0] # 这里的0是对切片后的字符串形成的列表list进行筛选，选第一段，即0（for in 就是对列表的）
            url_list.insert_one({'url': item_link })
            print(item_link)
    else:
        pass
#get_links_from('http://bj.58.com/shuma/', 2)

# spider 2 爬详情页的数据
