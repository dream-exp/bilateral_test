#coding:utf-8
from PIL import Image
from PIL import ImageOps
import math
import numpy as np

#画像の読み込み
im = Image.open("../images/Lenna.bmp")

#グレースケール変換
gray_im = ImageOps.grayscale(im)

# gray_im.show()

#画像サイズを取得
size = gray_im.size

#取得したサイズと同じ空のイメージを新規に作成
im2 = Image.new('L',size)
im3 = Image.new('L',size)
im4 = Image.new('L',size)

g_filter = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) #ガウシアンフィルタの配列

sigma1 = 20
sigma2 = 500

#loop
#x
for x in range(size[0]):
    #y
    for y in range(size[1]):

        #対象座標のピクセルを取得
        #5
        v5 = gray_im.getpixel((x,y))

        #初期化（とりあえず、全ての近傍値に現座標値をセット）
        v_value = np.array([[v5, v5, v5], [v5, v5, v5], [v5, v5, v5]])

        v_filter = np.zeros([3, 3])*1.0 #輝度差の重み付け用配列
        #g_filter = np.zeros([3, 3])*1.0 #ガウシアンフィルタの重み付け用配列

        #g_filter[1, 1] = math.exp(-((x)*(x)+(y)*(y)) / 2*(sigma1)*(sigma1))
        v_filter[1, 1] = math.exp(-(v_value[1, 1] - v_value[1, 1])*(v_value[1, 1] - v_value[1, 1]) / (2*(sigma2)*(sigma2)))

        #近傍座標の値を取得

        #1
        if x-1 > 0 and y+1 < size[1]:
            v_value[0, 0] = gray_im.getpixel((x-1,y+1))
            #g_filter[0, 0] = math.exp(-((x-1)*(x-1)+(y-1)*(y-1)) / 2*(sigma1)*(sigma1))
            v_filter[0, 0] = math.exp(-(v_value[1, 1] - v_value[0, 0])*(v_value[1, 1] - v_value[0, 0]) / (2*(sigma2)*(sigma2)))

        #2
        if y+1 < size[1]:
            v_value[1, 0] = gray_im.getpixel((x,y+1))
            #g_filter[1, 0] = math.exp(-((x)*(x)+(y-1)*(y-1)) / 2*(sigma1)*(sigma1))
            v_filter[1, 0] = math.exp(-(v_value[1, 1] - v_value[1, 0])*(v_value[1, 1] - v_value[1, 0]) / (2*(sigma2)*(sigma2)))

        #3
        if x+1 < size[0] and y+1 < size[1]:
            v_value[2, 0] = gray_im.getpixel((x+1,y+1))
            #g_filter[2, 0] = math.exp(-((x+1)*(x+1)+(y-1)*(y-1)) / 2*(sigma1)*(sigma1))
            v_filter[2, 0] = math.exp(-(v_value[1, 1] - v_value[2, 0])*(v_value[1, 1] - v_value[2, 0]) / (2*(sigma2)*(sigma2)))

        #4
        if x-1 > 0:
            v_value[0, 1] = gray_im.getpixel((x-1,y))
            #g_filter[0, 1] = math.exp(-((x-1)*(x-1)+(y)*(y)) / 2*(sigma1)*(sigma1))
            v_filter[0, 1] = math.exp(-(v_value[1, 1] - v_value[0, 1])*(v_value[1, 1] - v_value[0, 1]) / (2*(sigma2)*(sigma2)))

        #6
        if x+1 < size[0]:
            v_value[2, 1] = gray_im.getpixel((x+1,y))
            #g_filter[2, 1] = math.exp(-((x+1)*(x+1)+(y)*(y)) / 2*(sigma1)*(sigma1))
            v_filter[2, 1] = math.exp(-(v_value[1, 1] - v_value[2, 1])*(v_value[1, 1] - v_value[2, 1]) / (2*(sigma2)*(sigma2)))

        #7
        if x-1 > 0 and y-1 > 0:
            v_value[0, 2] = gray_im.getpixel((x-1,y-1))
            #g_filter[0, 2] = math.exp(-((x-1)*(x-1)+(y+1)*(y+1)) / 2*(sigma1)*(sigma1))
            v_filter[0, 2] = math.exp(-(v_value[1, 1] - v_value[0, 2])*(v_value[1, 1] - v_value[0, 2]) / (2*(sigma2)*(sigma2)))

        #8
        if y-1 > 0:
            v_value[1, 2] = gray_im.getpixel((x,y-1))
            #g_filter[1, 2] = math.exp(-((x)*(x)+(y+1)*(y+1)) / 2*(sigma1)*(sigma1))
            v_filter[1, 2] = math.exp(-(v_value[1, 1] - v_value[1, 2])*(v_value[1, 1] - v_value[1, 2]) / (2*(sigma2)*(sigma2)))

        #9
        if x+1 < size[0] and y-1 > 0:
            v_value[2, 2] = gray_im.getpixel((x+1,y-1))
            #g_filter[2, 2] = math.exp(-((x+1)*(x+1)+(y-1)*(y-1)) / 2*(sigma1)*(sigma1))
            v_filter[2, 2] = math.exp(-(v_value[1, 1] - v_value[2, 2])*(v_value[1, 1] - v_value[2, 2]) / (2*(sigma2)*(sigma2)))

        v_1 = 0 
        v_2 = 0 
        v_3 = 0 
        g_filter_sum = 0
        b_filter_sum = 0

        for i in range(3):
            for j in range(3):
                v_1 += v_value[i, j] * g_filter[i, j] #ガウシアンフィルタの分子
                v_2 += v_value[i, j]/9 #平均値フィルタの計算
                v_3 += v_value[i, j] * g_filter[i, j] * v_filter[i, j] #バイラテラルフィルタの分子
                g_filter_sum += g_filter[i, j] #ガウシアンフィルタの分母
                b_filter_sum += v_filter[i, j] * g_filter[i, j] #バイラテラルフィルタの分母
                # print v_3

        v_1_calc = v_1 / g_filter_sum
        v_3_calc = v_3 / b_filter_sum

        # print "v_3_calc"
        # print v_3_calc

        # print "v_value"
        # print v_value

        # print "v_3"
        # print v_3

        # print "v_filter"
        # print v_filter

        # print "v_filter_sum"
        # print v_filter_sum

        im2.putpixel((x,y), int(v_1_calc))
        im3.putpixel((x,y), int(v_2))
        im4.putpixel((x,y), int(v_3_calc))

#show
gray_im.save('input.bmp')
# im2.show()
im2.save('gaussian.bmp')
# im3.show()
im3.save('average.bmp')
im4.save('bilateral.bmp')