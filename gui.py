#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import tkinter
import tkinter.messagebox
from tkinter.filedialog import askdirectory
from tkinter import *
import requests   #对网页进行请求
from bs4 import BeautifulSoup   #网页解析库
import time
import os.path
import math
import socket

def main():
    #反斜杠转正斜杠
    def path2path(path):
        return path.replace('/', '\\\\')
    # 通过url获取文件名
    def file_name(path):
        return os.path.basename(path)
    # 抓取表情包核心函数
    def get_img(keyword,img_num,addr):
        path=path2path(addr)
        dicall = []
        hadget_num = 0
        isExists = os.path.exists(path)  # 判断路径是否存在，不存在则创建
        if not isExists:
            os.makedirs(path)
        start = time.time()
        pagenum = math.ceil(int(img_num) / 45)
        for i in range(0, int(pagenum), 1):
            url = 'https://www.fabiaoqing.com/search/search/keyword/' + keyword + '/type/bq/page/{}.html'.format(i + 1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}  # 或许有反爬措施，所以这里进行简单的处理，将我们的爬虫伪装成是人访问
            response = requests.get(url, headers=headers)  # 对网页进行请求并返回值
            html = response.text  # 将网页内容以html返回
            soup = BeautifulSoup(html, 'html.parser')  # 解析网页的一种方法
            img = soup.find_all('img', class_="lazy")  # 对表情包的定位
            count = soup.find_all('div', class_="tabular")
            count = re.sub("\D", "", count[0].find("a", class_="active").get_text())
            if int(count) / 45 < i:
                break;
            else:
                for n in range(len(img)):
                    if int(img_num)%45==n and (i+1)==int(pagenum):
                        break
                    dic = {}
                    dic['url'] = img[n].get('data-original')
                    dic['title'] = img[n].get('title')
                    dicall.append(dic)
                    try:
                        time.sleep(0.5)  # 延时处理，0.5s；根据情况调整
                        request = urllib.request.urlretrieve(dic['url'], path +'\\'+ file_name(dic['url']))
                        #print(request[1])
                        hadget_num=hadget_num+1
                        # color, msg = ('orange', '抓取中....,已抓取' + str(hadget_num) + '张')
                        # label_info.config(text=msg, fg=color)
                    except urllib.request.URLError as e:
                        print('-----URLError url:', e)
                    except socket.timeout as e:
                        print("-----socket timout:", e)
            response.close()
        end = time.time()
        runtime = end - start
        #print(runtime)
        color, msg = ('green', '已成功抓取' + str(hadget_num) + '张，耗时'+str(runtime)+'s')
        label_info.config(text=msg, fg=color)
    # 抓取前验证
    def get_before_check():
        keyword = b_keyword.get()  # 抓取表情包的关键字
        img_num = b_num.get()  # 要抓取的图片数量
        addr = b_addr.get()  # 图片保存路径
        if img_num=="":
            color, msg = ('red', '抓取数量不能为空')
            label_info.config(text=msg, fg=color)
        elif addr == "":
            color, msg = ('red', '请选择保存路径')
            label_info.config(text=msg, fg=color)
        else:
            color, msg = ('orange', '抓取中....')
            label_info.config(text=msg, fg=color)
            #time.sleep(5)
            get_img(keyword,img_num,addr)

    #输入框只能输入数字
    def check_num_f(content):
        if content.isdigit() or content == "":
            return True
        else:
            return False
    # 确认退出
    def confirm_to_quit():
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
            win.quit()
    #选择保存路径
    def select_dir():
        save_path = askdirectory();
        b_addr.set(save_path)  # 获取输入框内容

    # 创建顶层窗口
    win = tkinter.Tk()
    # 设置窗口大小
    win.geometry('300x200')
    # 设置窗口标题
    win.title('表情包爬虫-by Hokoa')
    # 禁止调整窗口大小
    win.resizable(0,0)
    # photo = tkinter.PhotoImage(format="gif",file="1.gif")
    # label_info1 = tkinter.Label(win, image=photo)
    # label_info1.place(x=300, y=0)

    #表情包关键字
    label_keyword = tkinter.Label(win, text='关键字：', font='YaHei 9', fg='green')
    label_keyword.place(x=20, y=20)
    #表情包关键字输入框
    b_keyword = tkinter.StringVar()
    b_input_keyword=tkinter.Entry(win, textvariable=b_keyword)
    b_input_keyword.place(x=80, y=20)

    # 表情包数量
    label_num = tkinter.Label(win, text='抓取数量：', font='YaHei 9', fg='green')
    label_num.place(x=20, y=50)
    # 表情包数量输入框
    check_num = win.register(check_num_f)
    b_num = tkinter.StringVar()
    b_input_num = tkinter.Entry(win, textvariable=b_num,validate='key',validatecommand=(check_num, '%P'))
    b_input_num.place(x=80, y=50)

    # 保存路径
    label_addr = tkinter.Label(win, text='保存地址：', font='YaHei 9', fg='green')
    label_addr.place(x=20, y=80)
    # 保存路径输入框
    b_addr = tkinter.StringVar()
    b_input_addr = tkinter.Entry(win, textvariable=b_addr,state='readonly')
    b_input_addr.place(x=80, y=80)
    #选择路径按钮
    button_addr = tkinter.Button(win, text='选择', command=select_dir)
    button_addr.place(x=230, y=75)

    # 信息提示
    label_info = tkinter.Label(win, text='未开始', font='YaHei 9', fg='red')
    label_info.place(x=20, y=110)

    # 创建一个装按钮的容器
    panel = tkinter.Frame(win)
    # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定事件回调函数
    button_getimg = tkinter.Button(panel, text='开始抓取', command=get_before_check)
    button_getimg.pack(side='left',padx="20")
    button_quit = tkinter.Button(panel, text='退出', command=confirm_to_quit)
    button_quit.pack(side='right',padx="20")
    panel.pack(side='bottom',pady="20")
    # 开启主事件循环
    tkinter.mainloop()
if __name__ == '__main__':
    main()
