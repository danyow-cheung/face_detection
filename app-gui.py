from genericpath import exists
from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
import os
names = list()

'''
主页面
'''
class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.split()
            for i in z:
                names.append(i)
            
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("人脸识别")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        
        # 容器/大布局
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        # 行列配置
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("退出", "确定退出"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                f.write(i+" ")
            self.destroy()

'''
起始页面：
    增加用户 识别用户 退出'''
class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller

            render = PhotoImage(file='homepage.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="主页", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew",ipadx=4)
            '''
            功能选项
                1.增加用户
                2.识别用户
                3.录入数据
                4.退出
            '''
            button1 = tk.Button(self, text="增加用户", fg="#263942", bg="#ffffff",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text=" 识别用户 ", fg="#263942", bg="#ffffff",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="退出", fg="#263942", bg="#ffffff", command=self.on_closing)
            
            # 布局
            button1.grid(row=1, column=0, ipady=2, ipadx=7)
            button2.grid(row=2, column=0, ipady=2, ipadx=7)
            button3.grid(row=3, column=0, ipady=2, ipadx=32)



        def on_closing(self):
            if messagebox.askokcancel("退出", "确定退出"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()

'''
增加用户：
    输入昵称 捕获图片以及训练模型'''
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="输入名称", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)

        
        # 录入没有数据的用户：功能补充
        self.buttonin = tk.Button(self, text="补录数据", fg="#263942", bg="#ffffff",command=self.input_data)
        # 取消返回上一页
        self.buttoncanc = tk.Button(self, text="取消", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        # 确定开始训练
        self.buttonext = tk.Button(self, text="创建", bg="#ffffff", fg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonin.grid(row=1,column=2, pady=10, ipadx=5, ipady=4)

    '''
    检错处理
    '''
    def start_training(self):
        global names
        
        new_name = self.user_name.get().replace(" ","")

        if  len(new_name) == 0 and new_name =="":
            messagebox.showinfo("错误", "名称不能为空")
            return
            
        elif new_name in names:
            messagebox.showinfo("错误", "用户已经存在")
            return
        else :
            messagebox.showinfo("成功","已创建新用户")
    

        name = new_name
        names.append(name)

        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")

    def input_data(self):
        global names
        user_name = self.user_name.get()

        if user_name in names:
            messagebox.showinfo("正确","开始录入数据")
        else:
            messagebox.showinfo("错误","未创建该用户")
            return
        self.controller.active_name = user_name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="选择用户", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        # 返回上一步按钮
        self.buttoncanc = tk.Button(self, text="取消", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        # 下一步按钮
        self.buttonext = tk.Button(self, text="确定", command=self.nextfoo, bg="#ffffff", fg="#263942")
        
        # 删除用户按钮
        self.buttondel = tk.Button(self,text="删除",command=self.delete_user, bg="#ffffff", fg="#263942")

        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttondel.grid(row=1,ipadx=5, ipady=4, column=2, pady=10)

    def nextfoo(self):
        
        if self.menuvar.get() == "None":
            messagebox.showinfo("错误", "名字不能为空")
            return
        
        else:
            self.controller.active_name = self.menuvar.get()
            self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))


    def delete_user(self):
        global names
        delete_user = self.menuvar.get()
        if delete_user:
           
            if not os.path.exists(f"data/classifiers/{delete_user}_classifier.xml"):
                messagebox.showinfo("提示",f"用户{delete_user}已删除")
            else:
                os.remove(f"data/classifiers/{delete_user}_classifier.xml")
            self.controller.show_frame("StartPage")
            
        else:
            messagebox.showinfo("错误", "名字不能为空")
            return 


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="已经捕获的数据量:0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        self.capturebutton = tk.Button(self, text="捕捉数据", bg="#ffffff", fg="#263942", command=self.capimg)

        self.trainbutton = tk.Button(self, text="训练模型", bg="#ffffff", fg="#263942",command=self.trainmodel)

        self.backbutton = tk.Button(self,text="主页",bg="#ffffff", fg="#263942",command=lambda :controller.show_frame("StartPage"))

        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.backbutton.grid(row=1,column=2, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("提示", "即将捕获人脸")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if not exists("data/{}"+self.controller.active_name):
            messagebox.showinfo("错误","未捕捉到数据")
            return


        if self.controller.num_of_images < 200:
            messagebox.showinfo("错误", "数据不足 至少捕获200张")
            return
        
        train_classifer(self.controller.active_name)
        messagebox.showinfo("成功", "模型训练成功")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="人脸识别", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        # 人脸识别api
        button1 = tk.Button(self, text="识别", command=self.openwebcam, bg="#ffffff", fg="#263942")

        button4 = tk.Button(self, text="主页", command=lambda: self.controller.show_frame("StartPage"), fg="#263942", bg="#ffffff")
               
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)


    def openwebcam(self):
        if not os.path.exists(f"data/classifiers/{self.controller.active_name}_classifier.xml"):
            messagebox.showinfo("错误","该用户没有数据")
            return
        else:
            main_app(self.controller.active_name)
            

app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

