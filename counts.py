import time
from page_parsing import url_list # url_list 是数据库的第一张表的名称

while True:
    print(url_list.find().count())
    # find()展示list中所有的元素，count()计数
    time.sleep(5)
# 该段程序用来监控用，当它和主程序一起开的时候，它可以计算数量进程，方便管理