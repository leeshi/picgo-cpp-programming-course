#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox as messagebox

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# here is how you should use uploader
from back import *


import matplotlib.pyplot as plt
from PIL import Image,ImageTk


uploader = ImageUploader()
uploader.set_imgur_api('6b75af0f94d844f',
        '0f45fb3d25a709ee76aabd9d4d72957b8c839985')

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='GO', command=self.go)
        self.alertButton.pack()
        '''
        self.canvas=Canvas(self,bg='blue',height=100,width=200)
        self.canvas.pack()
        '''

    def go(self):
        name = self.nameInput.get() 
        result = uploader.upload_image_imgur(name)
        
        img_open = Image.open(name)
        img_w=int(img_open.size[0]*0.1)
        img_h=int(img_open.size[1]*0.1)
        img_open=img_open.resize((img_w,img_h))
        #img_open.resize((100,200))
        img_png = ImageTk.PhotoImage(img_open)
        #img_png.resize((200,100))
        #image=self.canvas.create_image(0,0,anchor='nw',image=img_png)

        #self.lab=Label(self,image=img_png).pack()
        if result['status_code'] == 0:
            top = Toplevel()
            top.title('Python')
    
            v1 = StringVar()
            v1.set(result['url'])
            e1 = Entry(top,textvariable=v1,width=50).pack()
            #e1.grid(row=1,column=0,padx=1,pady=1)
    
            canvas=Canvas(top,bg='blue',height=img_h,width=img_w)
            canvas.pack()
            canvas.create_image(0,0,anchor='nw',image=img_png)
            top.mainloop()
        else:
            messagebox.showinfo('Message', result['msg'])
        #messagebox.showinfo('Message', 'Hello, %s' % name)
        '''
        top = Toplevel()
        top.title('Python')
 
        #v1 = StringVar()
        #e1 = Entry(top,textvariable=v1,width=10).pack()
        #e1.grid(row=1,column=0,padx=1,pady=1)
 
        canvas=Canvas(top,bg='blue',height=img_h,width=img_w)
        canvas.pack()
        canvas.create_image(0,0,anchor='nw',image=img_png)
        top.mainloop()
        '''
        '''
        if result['status_code'] == 0:
            messagebox.showinfo('Message', result['msg']+'---'+result['url'])
        else:
            messagebox.showinfo('Message', result['msg'])
        #messagebox.showinfo('Message', 'Hello, %s' % name)
        '''

app = Application()
# 设置窗口标题:
app.master.title('PICGO')
# 主消息循环:
app.mainloop()