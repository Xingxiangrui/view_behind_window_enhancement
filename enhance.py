"""
creted by xingxiangrui on 2019.7.4

   this program is to enhance the people behind the trunk glass
        click to select window
        histogram equalization to enahnce the peopel in the window

"""

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import cv2
import time

if_select_window = False
if_enhance_on_histogram = True


## ---------------------- click to select windows------------------
class click_to_select_windows():
    def __init__(self):
        self.img_path='photos/20190614093644644.jpg'

    def run_click_to_select_windows(self):
        def draw_rectangle(event,x,y,flags,param):
            global ix, iy, ox, oy
            if event==cv2.EVENT_LBUTTONDOWN:
                ix, iy = x, y
                print("point1:=", x, y)
            elif event==cv2.EVENT_LBUTTONUP:
                ox, oy= x, y
                print("point2:=", x, y)
                print("width=",x-ix)
                print("height=", y - iy)
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

        img=cv2.imread(self.img_path)
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

##-------------------------------------------------

##---------------- enhance histogram --------------------------
class enhance_on_histogram():
    def __init__(self):
        #self.img_path='photos/20190614082427627.jpg'
        self.img_path = click_to_select_windows().img_path
        if(if_select_window==True):
            self.window_left_top = (ix, ox)  # [x1,x2,y1,y2]
            self.window_right_down = (iy, oy)
        else:
            self.window_left_top=(57,209)      # [x1,x2,y1,y2]
            self.window_right_down=(403,381)
        self.if_show_original_img=False
        self.if_show_cuted_img = False
        self.if_show_equal_hist_cut_img=False
        self.if_save_enhanced_img=True
        self.equal_hist_or_adapt_hist=1 #equal hist is 0, adapt hist is 1

    def run_enhance_on_histogram(self):
        def show_img_and_space_to_break(img):
            while (1):
                cv2.imshow('image', img)
                if cv2.waitKey(1000) & 0xFF == ord(' '):
                    print("break")
                    break
            cv2.destroyAllWindows()


        # img windows
        img = cv2.imread(self.img_path)
        cv2.rectangle(img, self.window_left_top, self.window_right_down, (0, 255, 0), 2)

        # cv2.imshow('image', img)
        # cv2.waitKey(1000)
        # time.sleep(10)

        if self.if_show_original_img==True:
            while (1):
                cv2.imshow('image', img)
                if cv2.waitKey(1000) & 0xFF == ord(' '):
                    print("break")
                    break
            cv2.destroyAllWindows()

        # cut img
        cut_img=img[self.window_left_top[1]:self.window_right_down[1],self.window_left_top[0]:self.window_right_down[0]]

        if self.if_show_cuted_img==True:
            while (1):
                cv2.imshow('image', cut_img)
                if cv2.waitKey(1000) & 0xFF == ord(' '):
                    print("break")
                    break
            cv2.destroyAllWindows()

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

        if self.if_show_equal_hist_cut_img==True:
            show_img_and_space_to_break(img=result)

        if self.if_save_enhanced_img==True:
            if(self.equal_hist_or_adapt_hist==0):
                enhanced_img_path=self.img_path.replace(".jpg","enhanced.jpg")
            elif(self.equal_hist_or_adapt_hist==1):
                enhanced_img_path = self.img_path.replace(".jpg", "adaptive_enhanced.jpg")
            img[self.window_left_top[1]:self.window_right_down[1], self.window_left_top[0]:self.window_right_down[0]]=result
            cv2.imwrite(enhanced_img_path,img)



if __name__ == '__main__':


    if(if_select_window==True):
        print("run select window")
        click_to_select_windows().run_click_to_select_windows()

    if(if_enhance_on_histogram==True):
        print("run enhance on histogram")
        enhance_on_histogram().run_enhance_on_histogram()

    print("program done!")
