from multiprocessing import Pool #
from channel_extract import channel_list
from page_parsing import get_links_from, get_item_info, url_list, item_info

def get_all_links_from(channel):
    for num in range(1,51):
        get_links_from(channel,num)




if __name__=='__main__':   # 一种类似作文开头的感谢领导的套话格式，防止上下程序串混乱了，没特别的意思
    pool = Pool()  # 创建进程池
    pool.map(get_all_links_from, channel_list.split())
    # map函数的特点是把括号内的后一个参数放到前一个参数(函数)里去依次执行。约定俗成map第一个参数为不带 () 的函数。
    # channel_list 是引用过来的，我们之前定义过它是一个长字符串，将它分成一段段,split()函数会将一个字符串自动变成分割好的一个大list

# 断点续传
    db_urls = [ item['url'] for item in url_list.find() ]  # 用列表解析式装入所要爬取的链接
    index_urls = [ item['url'] for item in item_info.find() ]   # 所引出详情信息数据库中所有的现存的 url 字段,这里的item是一个字典，不是字典的方法 items()
    x = set(db_urls)     # 转换成集合的数据结构
    y = set(index_urls)    rest_of_urls = x - y  # 把这个链接替换到上面的pool.map的链接即可


# 设计思路：
# 1.分两个数据库，第一个用于只用于存放抓取下来的 url (ulr_list)；第二个则储存 url 对应的物品详情信息(item_info)
# 2.在抓取过程中在第二个数据库中写入数据的同时，新增一个字段(key) 'index_url' 即该详情对应的链接
# 3.若抓取中断，在第二个存放详情页信息的数据库中的 url 字段应该是第一个数据库中 url 集合的子集
# 4.两个集合的 url 相减得出圣贤应该抓取的 url 还有哪些
