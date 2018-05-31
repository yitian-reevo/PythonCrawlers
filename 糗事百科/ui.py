import tkinter as tk
import tkinter.messagebox
import webbrowser
from tkinter import END
from PIL import Image, ImageTk
import urllib.request

import db as datasourse
import qiushibaike as qb

def init_ui():
	root = tk.Tk()
	root.title('糗事百科私人阅读器')
	width = 600
	height = 440
	screenwidth = root.winfo_screenwidth()  
	screenheight = root.winfo_screenheight()  
	size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/3, (screenheight - height)/3)
	root.geometry(size)

	# 作者，好笑，评论字段
	lf_content = tk.LabelFrame(root, width=580, height=350)  
	lf_content.grid(row=0, column=0, sticky='w',padx=10, pady=10, columnspan=3)

	lstr_author = tk.StringVar()
	lstr_author.set("作者: ")
	lstr_fun_comment = tk.StringVar()
	lstr_fun_comment.set("0 好笑 0 评论")
	lstr_url = tk.StringVar()
	lstr_url.set("源地址：")
	lstr_url_val = tk.StringVar()
	href = ""

	label_author = tk.Label(lf_content,
		textvariable = lstr_author,
		width= 24, 
		height = 1,
		font = ('Microsoft YaHei', 12),
		anchor='w'
		)
	label_author.place(x=5, y=2)

	label_fun_comment = tk.Label(lf_content,
		textvariable = lstr_fun_comment,
		width= 24, 
		height = 1,
		font = ('Microsoft YaHei', 8),
		anchor='w'
		)
	label_fun_comment.place(x=5, y=30)

	label_url = tk.Label(lf_content,
		textvariable = lstr_url,
		width= 48, 
		height = 1,
		font = ('Microsoft YaHei', 10),
		anchor='w'
		)
	label_url.place(x=5, y=52)

	# 将URL做成可以点击的超链接
	def callback(event):
		global href
		webbrowser.open_new(href)

	label_url_val = tk.Label(lf_content,
		textvariable = lstr_url_val,
		fg='blue',
		cursor='hand2',
		width= 48, 
		height = 1,
		font = ('Microsoft YaHei', 10),
		anchor='w'
		)
	label_url_val.place(x=55, y=52)
	label_url_val.bind("<Button-1>", callback)

	# 文本组件
	textbox = tk.Text(lf_content, 
		width=62,
		height=12,
		relief='solid',
		font = ('Microsoft YaHei', 12),
		#state = 'disabled'
	)
	textbox.place(x=5,y=80)		

	# 进行1次爬取
	def button_spider_click():
		count = qb.OneCircleSpider()
		tk.messagebox.showinfo(title='HI', message='本次新抓取{0:d}了条记录。'.format(count))

	# 取一条记录并解析
	def button_luck_click():
		if 0 == datasourse.DBTotal():
			tk.messagebox.showinfo(title='HI', message='你已经看完了所有的百科，再抓一些吧！'.format(count))

		# 解析
		record = datasourse.DBquery()[0]
		lstr_author.set("作者: {0:s}".format(record['author']))
		lstr_fun_comment.set("{0:d} 好笑 {0:d} 评论".format(record['fun'], record['comment']))
		lstr_url_val.set(record['url'])
		global href
		href = record['url']

		# textbox在disabled状态下不能添加内容
		# 先改成normal，加完内容再改回来
		textbox.configure(state='normal')
		existed_text = textbox.get("1.0", END).strip()
		if existed_text:
			textbox.delete("1.0", END)
		textbox.insert('insert', record['content'])
		textbox.configure(state='disabled')

		# 无论如何先把图片按钮disable
		# 如果有图片，下载图片，enable图片按钮
		button_img.configure(state='disabled')
		if record['img_url']:
			urllib.request.urlretrieve(record['img_url'],filename='test.jpg')
			button_img.configure(state='normal')

	def button_img_click():
		# 新建一个窗口，大小和图片一样
		img_window = tk.Toplevel(root)
		img_window.title("图片查看")
		image = Image.open("test.jpg")
		# 这里为什么+4？为了对称
		img_window_size = '%dx%d+%d+%d' % (image.width + 4, image.height + 4, (screenwidth - image.width)/2, (screenheight - image.height)/2)
		img_window.geometry(img_window_size)
						
		img = ImageTk.PhotoImage(image)
		canvas = tk.Canvas(img_window, width = image.width ,height = image.height, bg = 'grey')
		# create_image()的前两个参数代表的是图片**中心**的坐标轴
		canvas.create_image(image.width//2, image.height//2, image=img)
		canvas.place(x=0,y=0)

		img_window.mainloop()

	# 三个按钮
	button_spider = tk.Button(root,
		text='抓取更多',
		width=10,
		height=2,
		font = ('Microsoft YaHei', 12),
		command=button_spider_click
		)
	button_spider.grid(row=1, column=0, sticky='we',padx=10)

	button_img = tk.Button(root,
		text='显示图片',
		width=10,
		height=2,
		font = ('Microsoft YaHei', 12),
		state = 'disabled',
		command=button_img_click
		)
	button_img.grid(row=1, column=1, sticky='we',padx=10)

	button_luck = tk.Button(root,
		text='手气不错',
		width=10,
		height=2,
		font = ('Microsoft YaHei', 12),
		command=button_luck_click
		)
	button_luck.grid(row=1, column=2, sticky='we',padx=10)

	root.mainloop()

if __name__ == '__main__':
	datasourse.DBconnect()
	init_ui()
	datasourse.DBclose()