import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import END
import webbrowser
import os.path

import smtp
import pinyin

mail_host = ''
mail_user = ''
mail_pass = ''
receiver  = ''
fullpath  = ''
bookname  = ''

class SentToKindleUI(object):
	def __init__(self, object):
		# 推送信息
		self.lf_sendinfo = tk.LabelFrame(object, width=256, height=144, text='推送信息')  
		self.lf_sendinfo.grid(row=0, column=0, sticky='w',padx=10)
		
		self.label_sendinfo_kindlemail = tk.Label(self.lf_sendinfo, width=12, text='Kindle邮箱：')
		self.label_sendinfo_kindlemail.place(x=5,y=2)
		self.label_sendinfo_entry1 = tk.Entry(self.lf_sendinfo, relief='solid')
		self.label_sendinfo_entry1.place(x=100, y=2)

		self.label_sendinfo_sendmail = tk.Label(self.lf_sendinfo, width=12, text='推送邮箱：')
		self.label_sendinfo_sendmail.place(x=5,y=30)
		self.label_sendinfo_entry2 = tk.Entry(self.lf_sendinfo, relief='solid')
		self.label_sendinfo_entry2.place(x=100, y=30)

		self.label_sendinfo_password = tk.Label(self.lf_sendinfo, width=12, text='推送邮箱密码：')
		self.label_sendinfo_password.place(x=5,y=58)
		self.label_sendinfo_entry3 = tk.Entry(self.lf_sendinfo, relief='solid',show='*')
		self.label_sendinfo_entry3.place(x=100, y=58)

		# 校验三个Entries的内容
		def label_sendinfo_bt_click():
			global mail_host, receiver, mail_user, mail_pass
			receiver  = self.label_sendinfo_entry1.get()
			mail_user = self.label_sendinfo_entry2.get()
			mail_pass = self.label_sendinfo_entry3.get()

			# 检查kindle邮箱
			if receiver.endswith('kindle.com') or receiver.endswith('kindle.cn'):
				pass
			else:
				tk.messagebox.showinfo(title='HI', message='Kindle邮箱必须以kindle.com或kindle.cn结尾。')
				self.label_sendinfo_entry1.delete(0, END)
				return

			# 检查推送邮箱	
			if mail_user.endswith('gmail.com'):
				mail_host = 'smtp.gmail.com'
			elif mail_user.endswith('163.com'):
				mail_host = 'smtp.163.com'
			elif mail_user.endswith('qq.com'):
				mail_host = 'smtp.qq.com'
			else:
				tk.messagebox.showinfo(title='HI', message='目前仅支持QQ、163和Gmail邮箱作为推送邮箱。')
				self.label_sendinfo_entry2.delete(0, END)
				self.label_sendinfo_entry3.delete(0, END)
				return

			# 如果能进行到这，说明内容校验都没问题
			tk.messagebox.showinfo(title='HI', message='输入没有问题！')


		varCheck = tk.IntVar()

		def label_sendinfo_checkbutton_click():
			if varCheck.get() == 1:
				self.label_sendinfo_entry3.config(show='')
			else:
				self.label_sendinfo_entry3.config(show='*')

		self.label_sendinfo_checkbutton = tk.Checkbutton(self.lf_sendinfo,
			text = '显示密码',
			variable = varCheck,
			onvalue = 1,
			offvalue = 0,
			command = label_sendinfo_checkbutton_click
			)
		self.label_sendinfo_checkbutton.place(x=90,y=86)

		self.label_sendinfo_bt = tk.Button(self.lf_sendinfo,
			text='校验',
			width=8,
			command=label_sendinfo_bt_click
			)
		self.label_sendinfo_bt.place(x=175,y=86)

		# 文件选择
		self.lf_file = tk.LabelFrame(object, width=256, height=128, text='文件选择')  
		self.lf_file.grid(row=1, column=0, sticky='w', padx=10)

		self.lf_file_label = tk.Label(self.lf_file, 
			width=34, 
			text='已选择：(空)',
			anchor='w', 
			justify='left',
			wraplength=240
			)
		

		def lf_file_bt_click():
			global bookname, fullpath
			SupportedFiletypes = [('所有文件','*.*'), ('mobi文件','*.mobi'), ('文本文件','*.txt'), ('pdf文件','*.pdf')] 
			filename = tk.filedialog.askopenfilename(filetypes=SupportedFiletypes)

			if filename != '':
				filesize = os.path.getsize(filename)/float(1024*1024)  # MB
				if float(filesize) > 50.00:
					tk.messagebox.showinfo(title='HI', message='文件大小不得超过50MB。')
					self.lf_file_label.config(text = '已选择：(空)')
					return
				self.lf_file_label.config(text = '已选择: '+ filename)
				fullpath = filename
				bookname = pinyin.get(os.path.basename(fullpath), format="numerical")

		self.lf_file_bt = tk.Button(self.lf_file,
			text = '选择文件',
			command=lf_file_bt_click
			)
		self.lf_file_bt.place(x=2, y=2)
		self.lf_file_label.place(x=2, y=42)

		# 描述信息
		self.lf_desc = tk.LabelFrame(object, width=256, height=96, text='说明')  
		self.lf_desc.grid(row=2, column=0, sticky='w', padx=10)

		def callback(event):
			webbrowser.open_new(r"https://journal.ethanshub.com/post/category/gong-cheng-shi/-python-kindledian-zi-shu-tui-song#toc_4")

		self.tmp = "目前一些使用的约束"
		self.lf_desc_label = tk.Label(self.lf_desc, 
			fg='blue',
			cursor='hand2',
			width=34, 
			text=self.tmp, 
			anchor='w', 
			justify='left',
			wraplength=250
			)
		self.lf_desc_label.place(x=2, y=2)
		self.lf_desc_label.bind("<Button-1>", callback)
		
		# 按钮
		self.lf_button = tk.Frame(object, width=256, height=96)  
		self.lf_button.grid(row=3, column=0, sticky='w', padx=10)

		def lf_button_bt1_click():
			global mail_host, mail_user, mail_pass, receiver, bookname
			
			smtp.SendToKindle(mail_host, mail_user, mail_pass, receiver, fullpath, bookname)

		self.lf_button_bt1 = tk.Button(self.lf_button,
			text='发送',
			width=12,
			height=2,
			command=lf_button_bt1_click
			)
		self.lf_button_bt1.place(x=20,y=5)

		self.lf_button_bt2 = tk.Button(self.lf_button,
			text='取消',
			width=12,
			height=2,
			command=self.lf_sendinfo.quit
			)
		self.lf_button_bt2.place(x=123,y=5)

# 初始化窗口
root = tk.Tk()
root.title('Sent to Kindle')

width = 276
height = 432
screenwidth = root.winfo_screenwidth()  
screenheight = root.winfo_screenheight()  
size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
root.geometry(size)

SentToKindleUI(root)
root.mainloop()