# view_behind_window_enhancement
enhance the view behind the window using CLAHE and euqal_hist


目的：增强车玻璃后的图像。车玻璃涉及反光等因素。

博主代码地址：

目录

一、图像读取与框选

1.1 图像读取

1.2 鼠标框选

1.3 直接框选

二、块内直方图均衡化

2.1 直方图均衡化

2.2 结果

三、限制直方图均衡化

3.1 CLAHE算法

3.2 程序

四、后续尝试超分辨率重建与reflection removal
一、图像读取与框选
1.1 图像读取

https://www.cnblogs.com/denny402/p/5096001.html

from PIL import Image

img=Image.open('photos/20190614082427627.jpg')
img.show()

1.2 鼠标框选

用鼠标选框暂时模拟目标检测流程，后续找出算法模拟玻璃框的定位。

https://blog.csdn.net/akadiao/article/details/80312254

参考

import cv2
def draw_rectangle(event,x,y,flags,param):
    global ix, iy
    if event==cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        print("point1:=", x, y)
    elif event==cv2.EVENT_LBUTTONUP:
        print("point2:=", x, y)
        print("width=",x-ix)
        print("height=", y - iy)
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

img = cv2.imread("max.png")  #加载图片
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)
while(1):
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()

[点击并拖拽以移动]

term端并不稳定

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import cv2

def draw_rectangle(event,x,y,flags,param):
    global ix, iy
    if event==cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        print("point1:=", x, y)
    elif event==cv2.EVENT_LBUTTONUP:
        print("point2:=", x, y)
        print("width=",x-ix)
        print("height=", y - iy)
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
	
img=cv2.imread('photos/20190614082427627.jpg')
#img.show()

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)

while(1):
    cv2.imshow('image', img)
    if cv2.waitKey(100) & 0xFF == ord(' '):
        break
		
#cv2.imshow('image', img)
#cv2.waitKey(0)

cv2.destroyAllWindows()

[点击并拖拽以移动]
1.3 直接框选

直接框选

        # cut img
        cut_img=img[self.window_left_top[1]:self.window_right_down[1],self.window_left_top[0]:self.window_right_down[0]]

合并与存储

        if self.if_save_enhanced_img==True:
            enhanced_img_path=self.img_path.replace(".jpg","enhanced.jpg")
            img[self.window_left_top[1]:self.window_right_down[1], self.window_left_top[0]:self.window_right_down[0]]=result
            cv2.imwrite(enhanced_img_path,img)

[点击并拖拽以移动]


二、块内直方图均衡化
2.1 直方图均衡化

        # equal hist
        (b, g, r) = cv2.split(cut_img)
        bH = cv2.equalizeHist(b)
        gH = cv2.equalizeHist(g)
        rH = cv2.equalizeHist(r)  # 合并每一个通道
        result = cv2.merge((bH, gH, rH))

[点击并拖拽以移动]
2.2 结果


[点击并拖拽以移动]


[点击并拖拽以移动]

[点击并拖拽以移动]

[点击并拖拽以移动]

[点击并拖拽以移动]

[点击并拖拽以移动]
三、限制直方图均衡化
3.1 CLAHE算法

https://www.cnblogs.com/jsxyhelu/p/6435601.html?utm_source=debugrun&utm_medium=referral

CLAHE与AHE不同的地方是对比度限幅，为了克服AHE的过度放大噪声的问题；

①设自适应直方图均衡化方法的滑动窗口大小为M*M，则局部映射函数为:

为滑动窗口局部直方图的累积分布函数(cumulative distribution function);

②的导数为直方图，从而局部映射函数的斜率S为:

故，限制直方图高度就等效于限制局部映射函数的斜率，进而限制对比度强度；

③设限定最大斜率为Smax，则允许的直方图高度最大为：

④对高度大于Hmax的直方图应截去多余的部分；

实际处理中，设截取阈值T(而非Hmax)对直方图进行截断，将截去的部分均匀的分布在整个灰阶范围上，以保证总的直方图面积不变，从而使整个直方图上升高度L，则有：

⑤最后改进的直方图为：

综上所述，改变最大的映射函数斜率Smax及相应的最大直方图高度Hmax，可获得不同增强效果的图像；

CLAHE通过限制局部直方图的高度来限制局部对比度的增强幅度，从而限制噪声的放大和局部对比度的过增强。
3.2 程序

http://cpuwdl.com/archives/17/

        # equal hist
        (b, g, r) = cv2.split(cut_img)

        if(self.equal_hist_or_adapt_hist==0):
            bH = cv2.equalizeHist(b)
            gH = cv2.equalizeHist(g)
            rH = cv2.equalizeHist(r)  # 合并每一个通道
        if(self.equal_hist_or_adapt_hist==1):
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            bH = clahe.apply(b)
            gH = clahe.apply(g)
            rH = clahe.apply(r)
        result = cv2.merge((bH, gH, rH))

[点击并拖拽以移动]
3.3 效果

明显优于直接直方图均衡。

[点击并拖拽以移动]

[点击并拖拽以移动]

[点击并拖拽以移动]

四、后续尝试超分辨率重建与reflection removal





