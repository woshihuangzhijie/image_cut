# -*- coding: utf-8 -*-
# @Author: huangzhijie
# @Date:   2017-08-30 11:32:31
# @Last Modified by:   huangzhijie
# @Last Modified time: 2017-08-31 13:44:05
from random import *
import requests


def getimg():

    url_list = []
    for i in range(98):
        num = random()
        print(num)
        url = "http://dean.pku.edu.cn/student/yanzheng.php?act=init&rand=" + str(num)
        url_list.append(url)
    # 获取图片
    x = 0
    for imgurl in url_list:
        try:
            img = requests.get(imgurl)
        except Exception as e:
            print(e, "图片无法下载")
            continue
        location = '/Users/huangzhijie/AnacondaProjects/CodeDemo/img/{0}.gif'.format(x)
        fp = open(location, 'wb')
        fp.write(img.content)
        fp.close()
        x += 1


if __name__ == '__main__':
    getimg()
