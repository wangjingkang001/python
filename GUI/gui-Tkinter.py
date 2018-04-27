#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import tkitner # python3中t为小写
from tkinter import * # 此写法，不用再库中方法名前面调用tkinter.Tk等

class tkinterTest(object):
	def __init__(self, master):
		super(tkinterTest, self).__init__()

		#1 主窗体大小设置
		master.geometry('400x200')

		#2 Frame 矩形区域，多用来作为容器  
		frame = Frame(master)  
		frame.pack()

		#3 label
		self.label = Label(master)
		self.label['text'] = 'this is text'
		self.label.pack()

		#4 Entry输入框
		self.text = StringVar()  
		self.text.set('change to what?')  
		self.entry = Entry(master)  
		self.entry['textvariable'] = self.text  
		self.entry.pack() 

		#5 button
		#注意这个地方，不要写成on_click(),如果是on_click()的话，会在mainloop中调用on_click函数，而不是单击button按钮时出发事件
		self.btn = Button(frame, text='Click me', command=self.on_click)

		#将按钮pack，充满整个窗体(只有pack的组件实例才能显示)
		# self.btn.pack(expand=YES, fill=BOTH)

		#此处side为LEFT表示将其放置 到frame剩余空间的最左方 
		self.btn.pack(side=LEFT)

		#6 下拉菜单
		menubar = Menu(master)
		#创建下拉菜单File，然后将其加入到顶级的菜单栏中  
		filemenu = Menu(menubar,tearoff=0)  
		filemenu.add_command(label="Open", command=self.hello)  
		filemenu.add_command(label="Save", command=self.hello)  
		filemenu.add_separator()  
		filemenu.add_command(label="Exit", command=master.quit)  
		menubar.add_cascade(label="File", menu=filemenu)  
		  
		#创建另一个下拉菜单Edit  
		editmenu = Menu(menubar, tearoff=0)  
		editmenu.add_command(label="Cut", command=self.hello)  
		editmenu.add_command(label="Copy", command=self.hello)  
		editmenu.add_command(label="Paste", command=self.hello)  
		menubar.add_cascade(label="Edit",menu=editmenu)  
		#创建下拉菜单Help  
		helpmenu = Menu(menubar, tearoff=0)  
		helpmenu.add_command(label="About", command=self.about)  
		menubar.add_cascade(label="Help", menu=helpmenu)  
		  
		#显示菜单  
		master.config(menu=menubar)


		#待补充...

	def on_click(self):
		self.label['text'] = 'change text'

	def hello(self):
		print('hello')  
  
	def about(self):  
		print('我是开发者')  
		



# 调用
win = Tk(className='gui_tkinter') # Tkinter库之中的函数（其实是类的构造函数，构造了一个对象）
tkinterTest(win)
win.mainloop() # 则是主窗口的成员函数，也就是表示让这个root工作起来，开始接收鼠标的和键盘的操作