"""
creted by xingxiangrui on 2019.7.11

   this program is to select out the bbox area and save


"""

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import cv2
import time
import os

if_save_img=True


## ---------------------- click to select windows------------------
class bbox_and_save():
    def __init__(self):
        self.input_dir_path="/home/xxr/trunk_enhancement/photos/"
        self.save_dir_path="/home/xxr/trunk_enhancement/photos/bbox_img/"

    def run_bbox_and_save(self):

        # all txt files
        if not os.path.isdir(self.save_dir_path):
            os.makedirs(self.save_dir_path)

        source_file_list = os.listdir(self.input_dir_path)

        # for all txt files
        for source_txt_name in source_file_list:
            if '.txt' in source_txt_name:
                print(source_txt_name)

                # read images
                source_img_name=source_txt_name.replace(".txt","adaptive_enhanced.jpg")
                path_source_img = os.path.join(self.input_dir_path, source_img_name)
                src_img = cv2.imread(path_source_img)

                # read bbox
                txt_file=open(self.input_dir_path+source_txt_name,'r')
                lines = txt_file.readlines()
                for line in lines:
                    line=line.split(' ')
                cut_img = src_img[int(line[1]):int(line[3]),int(line[0]):int(line[2])]

                #save cuted img
                cut_img_name=source_txt_name.replace(".txt","_cut.jpg")
                path_cut_img=self.save_dir_path+cut_img_name
                #cut_img.save(path_cut_img)
                cv2.imwrite(path_cut_img, cut_img)

if __name__ == '__main__':

    bbox_and_save().run_bbox_and_save()
    print("program done!")


