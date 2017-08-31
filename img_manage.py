# -*- coding: utf-8 -*-
# @Author: huangzhijie
# @Date:   2017-08-30 12:46:33
# @Last Modified by:   huangzhijie
# @Last Modified time: 2017-08-31 13:43:59

from PIL import Image, ImageDraw
import sys
import random
class Img_Manage(object):
    # 去除噪点
    def sum_9_region(self, img, x, y):
        """
        9邻域框,以当前点为中心的田字框,黑点个数
        :param x:
        :param y:
        :return:
        """
        # todo 判断图片的长宽度下限
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.size[0]
        height = img.size[1]

        if cur_pixel == 255:  # 如果当前点为白色区域,则不统计邻域值
            return 9

        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = (cur_pixel 
                       +img.getpixel((x, y + 1))
                       + img.getpixel((x + 1, y))
                       + img.getpixel((x + 1, y + 1)))
                return 4 - sum / 255
            elif x == width - 1:  # 右上顶点
                sum = (cur_pixel
                       + img.getpixel((x, y + 1))
                       + img.getpixel((x - 1, y))
                       + img.getpixel((x - 1, y + 1)))

                return 4 - sum / 255
            else:  # 最上非顶点,6邻域
                sum = (img.getpixel((x - 1, y))
                       + img.getpixel((x - 1, y + 1))
                       + cur_pixel
                       + img.getpixel((x, y + 1))
                       + img.getpixel((x + 1, y))
                       + img.getpixel((x + 1, y + 1)))
                return 6 - sum / 255
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = (cur_pixel
                       + img.getpixel((x + 1, y))
                       + img.getpixel((x + 1, y - 1))
                       + img.getpixel((x, y - 1)))
                return 4 - sum / 255
            elif x == width - 1:  # 右下顶点
                sum = (cur_pixel
                       + img.getpixel((x, y - 1))
                       + img.getpixel((x - 1, y))
                       + img.getpixel((x - 1, y - 1)))

                return 4 - sum / 255
            else:  # 最下非顶点,6邻域
                sum = (cur_pixel
                       + img.getpixel((x - 1, y))
                       + img.getpixel((x + 1, y))
                       + img.getpixel((x, y - 1))
                       + img.getpixel((x - 1, y - 1))
                       + img.getpixel((x + 1, y - 1)))
                return 6 - sum / 255
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = (img.getpixel((x, y - 1))
                       + cur_pixel
                       + img.getpixel((x, y + 1))
                       + img.getpixel((x + 1, y - 1))
                       + img.getpixel((x + 1, y))
                       + img.getpixel((x + 1, y + 1)))

                return 6 - sum / 255
            elif x == width - 1:  # 右边非顶点
                # print('%s,%s' % (x, y))
                sum = (img.getpixel((x, y - 1))
                       + cur_pixel
                       + img.getpixel((x, y + 1))
                       + img.getpixel((x - 1, y - 1))
                       + img.getpixel((x - 1, y))
                       + img.getpixel((x - 1, y + 1)))

                return 6 - sum / 255
            else:  # 具备9领域条件的
                sum = (img.getpixel((x - 1, y - 1))
                       + img.getpixel((x - 1, y))
                       + img.getpixel((x - 1, y + 1))
                       + img.getpixel((x, y - 1))
                       + cur_pixel
                       + img.getpixel((x, y + 1))
                       + img.getpixel((x + 1, y - 1))
                       + img.getpixel((x + 1, y))
                       + img.getpixel((x + 1, y + 1)))
                return 9 - sum / 255

    def cut_letter(self, img, start, end):
        # 从靠近中轴线的白点开始出发
        mid = (start + end) // 2 - 2
        while img.getpixel((mid, 0)) == 0:
            mid += 1
        cut_line = []

        def cut(x, y):
            cut_line.append((x, y))
            if y == img.size[1] - 1:
                return
            #print(x, y)
            if (img.getpixel((x - 1, y + 1)) == img.getpixel((x, y + 1)) and
                    img.getpixel((x, y + 1)) == img.getpixel((x + 1, y + 1))):
                # www
                if img.getpixel((x - 1, y + 1)) == 255:
                    cut(x , y + 1)
                # bbb
                else:
                    cut(x , y + 1)
            elif (img.getpixel((x - 1, y + 1)) == img.getpixel((x, y + 1)) and
                    img.getpixel((x, y + 1)) != img.getpixel((x + 1, y + 1))):
                # wwb
                if img.getpixel((x - 1, y + 1)) == 255:
                    cut(x, y + 1)
                # bbw
                else:
                    cut(x + 1, y + 1) 
            elif (img.getpixel((x - 1, y + 1)) != img.getpixel((x, y + 1)) and
                    img.getpixel((x, y + 1)) == img.getpixel((x + 1, y + 1))):
                # wbb
                if img.getpixel((x - 1, y + 1)) == 255:
                    cut(x - 1, y + 1)
                # bww
                else:
                    cut(x, y + 1)
            elif (img.getpixel((x - 1, y + 1)) == img.getpixel((x + 1, y + 1)) and
                    img.getpixel((x, y + 1)) != img.getpixel((x + 1, y + 1))):
                # wbw
                if img.getpixel((x - 1, y + 1)) == 255:
                    cut(x + 1, y + 1)
                # bwb
                else:
                    cut(x, y + 1)
        cut(mid, 0)
        return cut_line
    def cut_image(self, img_file):
        im = Image.open(img_file)
        # 查看图片的格式
        #print(im.size, im.mode, im.format)
        # 将图片转化为8位像素模式
        # im.convert("P")
        # print(im.histogram())
        im2 = Image.new("P", im.size, 255)
        # 二值化
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                pix = im.getpixel((x, y))
                if pix == 6 or pix == 7 or pix == 8 or pix == 9:
                    im2.putpixel((x, y), 0)
        # im2.show()
        img = Image.new("P", im2.size, 255)
        # 去除孤立点
        for x in range(im2.size[0]):
            for y in range(im2.size[1]):
                Count = self.sum_9_region(im2, x, y)
                if Count >= 7:
                    img.putpixel((x, y), 255)
                else:
                    img.putpixel((x, y), 0)
        # print(img.histogram())
        # img.show()
        # 将图像进行切割，这里的图像有粘连，先直接纵向切割；
        inletter = False
        foundletter = False
        start = 0
        end = 0
        letters = []
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix = img.getpixel((x, y))
                if pix == 0:
                    inletter = True
            if foundletter is False and inletter is True:
                foundletter = True
                start = x
            if foundletter is True and inletter is False:
                foundletter = False
                end = x
                letters.append((start, end))
            inletter = False
        #print(letters)
        cut_lines = []
        for i in range(1, len(letters)):
            cut_lines.append([(letters[i - 1][1] + letters[i][0]) // 2])
        if len(letters) < 4:
            for letter in letters:
                if letter[1] - letter[0] > 10:
                    cut_lines.append(self.cut_letter(img, letter[0], letter[1]))
        #print(cut_lines)
        for i in cut_lines:
            if len(i) > 1:
                draw = ImageDraw.Draw(img)
                draw.line(i,fill = 100)
                del draw
        #img.show()
        return img
if __name__ == '__main__':
    ImageObject = Img_Manage()
    for x in range(10):
        s = random.randint(0, 98)
        img_file = 'img/{}.gif'.format(s)
        ImageObject.cut_image(img_file).show()