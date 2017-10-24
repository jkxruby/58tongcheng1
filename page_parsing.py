from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
chengxu = client['chengxu']
url_list = chengxu['url_list3']
item_info = url_list['item_info3']

# spider 1 爬取首页中显示的类目中，一个类目下的所有商品的链接
def get_links_from(channel,pages,who_sells=0): # who_sells = 0表示个人，1表示商家
    #http://bj.58.com/shouji/1/pn2/
    list_view = '{}{}/pn{}/'.format(channel,str(who_sells),str(pages)) # 找网页规律的时候，刚刷新和点击后的相同页面的网址会有变化，但页面相同，它们是等价的，所以找页面规律时要多点击或刷新来找
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('td','t'):  # 一个类目的页码是有限的，通过寻找td.t来判断系统是否爬过头了
        for link in soup.select('td.t  a.t'):  # 这里的td.t a.t 是点击某个分类后的新网页的每个具体商品的链接的selector
        #for link in soup.select( ('td.t a.t') if not soup.find_all('zhiding', 'huishou') else None ): #修改失败，计划排除被抓取的几排广告
            # 注意!!!上面代码后面，若是('td.t >a.t')即无法显示结果，必须空格！这样才对('td.t > a.t')

            item_link = link.get('href').split('?')[0] # 这里的0是对切片后的字符串形成的列表list进行筛选，选第一段，即0（for in 就是对列表的）
            url_list.insert_one({'url': item_link }) # insert是数据库函数，注意区分
            print(item_link)
    else:
        pass
#get_links_from('http://bj.58.com/shuma/', 2)

# spider 2 爬详情页的数据
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = '商品已下架' in soup.find('div', "button_li").get_text() # 从下方 AAA 处移过来的代码，理解时先忽略它。
    # find()里面的代码实际是完整的div="button_li",而且要保证该段代码在正常网页和已下架网页中都存在，否则正常网页报错。
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('span.price_now i')[0].text
        # 后面必须加[0].text,因为数据库要是str才能存进去，soup.select返回的对象是list，就算list里面只有一个元素，也不能用.text方法，所以才选择用[0],把元素从list调出来，再进行.text方法
        area = soup.select('.palce_li i')[0].text if soup.find_all('i') else None
        item_info.insert_one({'title':title, 'price':price, 'area':area })
        print({'title': title, 'price': price, 'area':area})

#get_item_info('http://zhuanzhuan.58.com/detail/919823388320399372z.shtml')

#======= AAA 爬取的商品链接中有失效的，剔除它(商品已交易则该网址会失效)，测试完该段代码备注掉==========#
# url = 'http://zhuanzhuan.58.com/detail/922439089107222541z.shtml'  # 网址上的商品已下架
# wb_data = requests.get(url)
# soup = BeautifulSoup(wb_data.text, 'lxml')
#print(soup.prettify())

# 上面的步骤查询了失效网址的结构。
#no_longer_exist = '商品已下架' in soup.find('span', "soldout_btn").get_text()  # 搬到上方get_item_info
#print (no_longer_exist) # 查看no_longer_exist是True False。上面的find里代码必须是完整的<xxx>内容，形成一个list，否则系统报错属性错误或者无法迭代







