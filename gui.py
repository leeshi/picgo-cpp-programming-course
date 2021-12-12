# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
from back import *
import numpy as np
from back.model import ImageModel
from io import BytesIO
model = ImageModel('./my.db')
uploader = ImageUploader()
uploader.set_imgur_api('6b75af0f94d844f',
        '0f45fb3d25a709ee76aabd9d4d72957b8c839985')




class GuiSample(object):

    def __init__(self):
        self.root = tk.Tk()

        # 设置GUI界面属性
        self.root.title('图片寻址应用')  # 设置GUI标题
        self.root.wm_attributes("-alpha", 1.0)  # 设置GUI透明度(0.0~1.0)
        self.root.wm_attributes("-topmost", True)  # 设置GUI置顶
        # self.root.wm_attributes("-toolwindow", True)  # 设置为工具窗口（没有放大和缩小按钮）
        # self.root.overrideredirect(-1)  # 去除GUI边框（GUI标题、放大缩小和关闭按钮都会消失）
        # self.bind_window_move_events()  # 如果去除GUI边框了，就要绑定窗口移动事件，否则GUI无法移动
        self.build_button()

        self.add_new_window_Upload.grid(row=1, column=0, sticky=tk.W)
        self.add_new_window_Search.grid(row=2, column=0, sticky=tk.W)
        self.add_new_window_all_photo.grid(row=3, column=0, sticky=tk.W)
        self.quit_button.grid(row=4, column=0, sticky=tk.W)

        self.set_gui_geometry(window=self.root)


    def build_button(self):
        """
        构建点击按钮控件
        :return:
        """
        self.quit_button = tk.Button(self.root, text='Quit', command=self.tk_quit, bg='tomato')
        self.add_new_window_Upload = tk.Button(self.root, text='Upload', command=self.new_window_Upload, bg='PeachPuff')
        self.add_new_window_Search = tk.Button(self.root, text='Search', command=self.new_window_Search, bg='PeachPuff')
        self.add_new_window_all_photo = tk.Button(self.root, text='All photo', command=self.new_window_all_photo, bg='PeachPuff')

        
    def tk_quit(self):
        self.root.destroy()  # 销毁当前窗口
        self.root.quit()  # 退出GUI

    def new_window_Upload(self):
        """
        在主窗口上添加一个新的窗口
        :return:
        """

        self.window = tk.Toplevel(self.root)  # 设置self.root为主窗口
        self.window.title('Upload Window')
        self.window.wm_attributes("-topmost", True)  # 设置新窗口置顶

        self.path=tk.StringVar()
        self.url=tk.StringVar()
        self.choosepic_Button=tk.Button(self.window,text='选择图片',command=self.choosepic).grid(row=1, column=0)
        tk.Label(self.window, text='本地路径').grid(row=2, column=0)
        self.local_path=tk.Entry(self.window,state='readonly',text=self.path)
        self.local_path.grid(row=3, column=0)
        self.go_Button = tk.Button(self.window, text='GO', command=self.go).grid(row=4, column=0)
        tk.Label(self.window, text='url路径').grid(row=5, column=0)
        
        self.local_url=tk.Entry(self.window,state='readonly',text=self.url)
        self.local_url.grid(row=6, column=0)
        self.local_photo=tk.Label(self.window)
        self.local_photo.grid(row=7, column=0)
        
        self.return_confirm = tk.Button(self.window, text='Return', command=self.window.destroy, bg='MediumSpringGreen')
        self.return_confirm.grid(row=1, column=1)
        self.set_gui_geometry(window=self.window, x=1.6, y=3.5)

    def new_window_all_photo(self):
        """
        在主窗口上添加一个新的窗口
        :return:
        """

        self.window2 = tk.Toplevel(self.root)  # 设置self.root为主窗口
        self.window2.title('all Window')
        self.window2.wm_attributes("-topmost", True)  # 设置新窗口置顶



        self.IMG=[]
        self.ALLURL=[]
        self.ALLNAME=[]
        self.counter=0
        self.all_img=model.get_all_images()
        for i in range(0,len(self.all_img)):
            img=Image.fromarray((plt.imread(BytesIO(self.all_img[i][0]))*255).astype(np.uint8))
            img=img.resize((350,350),Image.ANTIALIAS)
            img=ImageTk.PhotoImage(img)
            self.IMG.append(img)
        for i in range(0,len(self.all_img)):
            url=self.all_img[i][3]
            self.ALLURL.append(url)
        for i in range(0,len(self.all_img)):
            other_name=self.all_img[i][2]
            self.ALLNAME.append(other_name)
        
        



        self.all_url=tk.StringVar()
        self.all_url.set(self.ALLURL[0])
        self.local_all_url=tk.Entry(self.window2,state='readonly',text=self.all_url)
        self.local_all_url.grid(row=0, column=0)

        self.all_num=tk.StringVar()
        self.all_num.set("1/"+str(len(self.all_img)))
        self.local_all_num=tk.Entry(self.window2,state='readonly',text=self.all_num)
        self.local_all_num.grid(row=1, column=0)

        self.all_name=tk.StringVar()
        self.all_name.set(self.ALLNAME[0])
        self.local_all_name=tk.Entry(self.window2,state='readonly',text=self.all_name)
        self.local_all_name.grid(row=2, column=0)

        self.all_photo_num=self.IMG[0]
        self.all_photo=tk.Label(self.window2,image=self.all_photo_num)
        self.all_photo.grid(row=3, column=0)


        self.next_photo = tk.Button(self.window2, text='Next => ', command=self.next_all_photo)
        self.next_photo.grid(row=0, column=1)

        self.last_photo = tk.Button(self.window2, text='Last <=', command=self.last_all_photo)
        self.last_photo.grid(row=0, column=2)

        self.return_confirm = tk.Button(self.window2, text='Return', command=self.window2.destroy, bg='MediumSpringGreen')
        self.return_confirm.grid(row=0, column=3)
        self.set_gui_geometry(window=self.window2, x=1.6, y=3.5)


    def new_window_Search(self):
        """
        在主窗口上添加一个新的窗口
        :return:
        """
        self.IMGS=[]
        self.SEARCHURL=[]
        self.SEARCHNAME=[]
        self.search_counter=0

        self.window3 = tk.Toplevel(self.root)  # 设置self.root为主窗口
        self.window3.title('Search Window')
        self.window3.wm_attributes("-topmost", True)  # 设置新窗口置顶

        self.search_url=tk.StringVar()
        
        self.local_search_url=tk.Entry(self.window3,state='readonly',text=self.search_url)
        self.local_search_url.grid(row=1, column=0)

        self.search_num=tk.StringVar()
        
        self.local_search_num=tk.Entry(self.window3,state='readonly',text=self.search_num)
        self.local_search_num.grid(row=2, column=0)

        self.search_name=tk.StringVar()
        
        self.local_search_name=tk.Entry(self.window3,state='readonly',text=self.search_name)
        self.local_search_name.grid(row=3, column=0)



        self.v = tk.StringVar()
        self.e = tk.Entry(self.window3, textvariable=self.v)
        self.e.grid(row=0, column=0)

        self.search_photo = tk.Button(self.window3, text='search', command=self.search_photo)
        self.search_photo.grid(row=0, column=1)

        self.next_search_photo = tk.Button(self.window3, text='Next => ', command=self.next_search_photo)
        self.next_search_photo.grid(row=0, column=2)

        self.last_search_photo = tk.Button(self.window3, text='Last <=', command=self.last_search_photo)
        self.last_search_photo.grid(row=0, column=3)      

        self.return_confirm = tk.Button(self.window3, text='Return', command=self.window3.destroy, bg='MediumSpringGreen')
        self.return_confirm.grid(row=0, column=4)

        self.set_gui_geometry(window=self.window3, x=1.6, y=3.5)

    def search_photo(self):
        self.IMGS=[]
        self.SEARCHURL=[]
        self.SEARCHNAME=[]
        self.search_counter=0
        self.search_img=model.search_alias(self.e.get())
        for i in range(0,len(self.search_img)):
            img=Image.fromarray((plt.imread(BytesIO(self.search_img[i][0]))*255).astype(np.uint8))
            img=img.resize((350,350),Image.ANTIALIAS)
            img=ImageTk.PhotoImage(img)
            self.IMGS.append(img)
        self.all_photo=tk.Label(self.window3,image=self.IMGS[self.search_counter])
        self.all_photo.grid(row=4, column=0)
        for i in range(0,len(self.search_img)):
            url=self.search_img[i][3]
            self.SEARCHURL.append(url)
        for i in range(0,len(self.search_img)):
            other_name=self.search_img[i][2]
            self.SEARCHNAME.append(other_name)
        self.search_url.set(self.SEARCHURL[0])
        self.search_num.set("1/"+str(len(self.search_img)))
        self.search_name.set(self.SEARCHNAME[0])
        self.search_photo_num=self.IMGS[0]
        



    def next_all_photo(self):
        if(self.counter+1)<(len(self.all_img)):
            self.counter+=1
        else:
            self.counter=0
       
            
        self.all_photo=tk.Label(self.window2,image=self.IMG[self.counter])
        self.all_photo.grid(row=3, column=0)
        self.all_url.set(self.ALLURL[self.counter])
        self.all_name.set(self.ALLNAME[self.counter])
        self.all_num.set(str(self.counter+1)+"/"+str(len(self.all_img)))


    def last_all_photo(self):
        if(self.counter-1)>=0:
            self.counter-=1
        else:
            self.counter=len(self.all_img)-1
        
        self.all_photo=tk.Label(self.window2,image=self.IMG[self.counter])
        self.all_photo.grid(row=3, column=0)
        self.all_url.set(self.ALLURL[self.counter])
        self.all_name.set(self.ALLNAME[self.counter])
        self.all_num.set(str(self.counter+1)+"/"+str(len(self.all_img)))


    def next_search_photo(self):

        if(self.search_counter+1)<len(self.search_img):
            self.search_counter+=1
        else:
            self.search_counter=0
        
        self.search_photo_num=tk.Label(self.window3,image=self.IMGS[self.search_counter])
        self.search_photo_num.grid(row=4, column=0)
        self.search_url.set(self.SEARCHURL[self.search_counter])
        self.search_name.set(self.SEARCHNAME[self.search_counter])
        self.search_num.set(str(self.search_counter+1)+"/"+str(len(self.search_img)))
        


    def last_search_photo(self):
        if(self.search_counter-1)>=0:
            self.search_counter-=1
        else:
            self.search_counter=len(self.search_img)-1
        
        self.search_photo_num=tk.Label(self.window3,image=self.IMGS[self.search_counter])
        self.search_photo_num.grid(row=4, column=0)
        self.search_url.set(self.SEARCHURL[self.search_counter])
        self.search_name.set(self.SEARCHNAME[self.search_counter])
        self.search_num.set(str(self.search_counter+1)+"/"+str(len(self.search_img)))



    def choosepic(self):
        self.path_=askopenfilename()
        self.path.set(self.path_)
        self.img_open = Image.open(self.local_path.get())
        self.img_open=self.img_open.resize((350,350),Image.ANTIALIAS)
        self.img=ImageTk.PhotoImage(self.img_open)
        self.local_photo.config(image=self.img)
        self.local_photo.image=self.img #keep a reference

    def go(self):
        name = self.local_path.get()
        data=name.split('/')[-1]
        #print(name)
        #print(data)
        result = uploader.upload_image_imgur(name)
        if result['status_code'] == 0:
            self.url.set(result['url'])
        else:
            messagebox.showinfo('Message', result['msg'])
        model.save_image(name,result['url'],data)

    @staticmethod
    def set_gui_geometry(window, x=2.5, y=4.0):
        """
        设置window的几何分布，可以控制x轴和y轴的位置
        :param window:
        :param x: x轴位置
        :param y: y轴位置
        :return:
        """
        window.update_idletasks()
        x_info = (window.winfo_screenwidth() - window.winfo_reqwidth()) / x
        y_info = (window.winfo_screenwidth() - window.winfo_reqwidth()) / y
        window.geometry('+%d+%d' % (x_info, y_info))

if __name__ == '__main__':
    guiSample = GuiSample()
    guiSample.root.mainloop()
