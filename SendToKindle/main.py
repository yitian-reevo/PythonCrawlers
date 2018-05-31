import ui as myUI

# 初始化窗口
root = myUI.tk.Tk()
root.title('Sent to Kindle')

width = 276
height = 432
screenwidth = root.winfo_screenwidth()  
screenheight = root.winfo_screenheight()  
size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
root.geometry(size)

myUI.SentToKindleUI(root)
root.mainloop()