from multiprocessing import Pool #
from channel_extract import channel_list
from page_parsing import get_links_from

def get_all_links_from(channel):
    for num in range(1,51):
        get_links_from(channel,num)




if __name__=='__main__':   # 一种类似作文开头的感谢领导的套话格式，防止上下程序串混乱了，没特别的意思
    pool = Pool()  # 创建进程池
    pool.map(get_all_links_from, channel_list.split())
    # map函数的特点是把括号内的后一个参数放到前一个参数(函数)里去依次执行。约定俗成map第一个参数为不带 () 的函数。
    # channel_list 是引用过来的，我们之前定义过它是一个长字符串，将它分成一段段,split()函数会将一个字符串自动变成分割好的一个大list
