import requests
import re
import argparse
import sys
import json
import os
import threading
import traceback

import urllib
import tkinter
import tkinter.messagebox
from tkinter.filedialog import askdirectory
from tkinter import ttk
from tkinter import *
import requests  # 对网页进行请求
from bs4 import BeautifulSoup  # 网页解析库
import time
import os.path
import math
import socket


# 根据文件决定函数
y = 0
lb = ""


def main():
    def confirm_to_quit():
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
            win.quit()
    def run_start():
        def get_success(*info):
            tkinter.messagebox.showinfo("获取成功", "获取成功！\n" + str(info))

        def DOC(url):
            doc_id = re.findall('view/(.*).html', url)[0]
            html = requests.get(url).text
            lists = re.findall('(https.*?0.json.*?)\\\\x22}', html)
            lenth = (len(lists)//2)
            NewLists = lists[:lenth]
            for i in range(len(NewLists)):
                NewLists[i] = NewLists[i].replace('\\', '')
                txts = requests.get(NewLists[i]).text
                txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', txts)
                for i in range(0, len(txtlists)):
                    global y
                    lb.insert(END, txtlists[i][0].encode(
                        'utf-8').decode('unicode_escape', 'ignore')+"\n")
                    lb.see(END)
                    # print()
                    if y != txtlists[i][1]:
                        y = txtlists[i][1]
                        n = '\n'
                    else:
                        n = ''
                    filename = doc_id + '.txt'
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(
                            n+txtlists[i][0].encode('utf-8').decode('unicode_escape', 'ignore').replace('\\', ''))
            lb.insert(END, "文档保存在"+filename+"\n")
            lb.see(END)
            get_success("文档保存在"+filename)

        def PPT(url):
            doc_id = re.findall('view/(.*).html', url)[0]
            url = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + \
                doc_id+"&pn=1&rn=99999&type=ppt"
            html = requests.get(url).text
            lists = re.findall('{"zoom":"(.*?)","page"', html)
            for i in range(0, len(lists)):
                lists[i] = lists[i].replace("\\", '')
            try:
                os.mkdir(doc_id)
            except:
                pass
            for i in range(0, len(lists)):
                img = requests.get(lists[i]).content
                with open(doc_id+'\img'+str(i)+'.jpg', 'wb') as m:
                    m.write(img)
            lb.insert(END, "PPT图片保存在" + doc_id + "文件夹"+"\n")
            lb.see(END)
            get_success("PPT图片保存在" + doc_id + "文件夹")

        def TXT(url):
            doc_id = re.findall('view/(.*).html', url)[0]
            url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id="+doc_id
            html = requests.get(url).text
            md5 = re.findall('"md5sum":"(.*?)"', html)[0]
            pn = re.findall('"totalPageNum":"(.*?)"', html)[0]
            rsign = re.findall('"rsign":"(.*?)"', html)[0]
            NewUrl = 'https://wkretype.bdimg.com/retype/text/' + \
                doc_id+'?rn='+pn+'&type=txt'+md5+'&rsign='+rsign
            txt = requests.get(NewUrl).text
            jsons = json.loads(txt)
            texts = re.findall("'c': '(.*?)',", str(jsons))
            lb.insert(END, texts)
            lb.see(END)
            filename = doc_id+'.txt'
            with open(filename, 'a', encoding='utf-8') as f:
                for i in range(0, len(texts)):
                    texts[i] = texts[i].replace('\\r', '\r')
                    texts[i] = texts[i].replace('\\n', '\n')
                    f.write(texts[i])
            lb.insert(END, "\n"+"文档保存在" + filename+"\n")
            lb.see(END)
            get_success("文档保存在" + filename)

        def PDF(url):
            doc_id = re.findall('view/(.*).html', url)[0]
            url = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + \
                doc_id+"&pn=1&rn=99999&type=ppt"
            html = requests.get(url).text
            lists = re.findall('{"zoom":"(.*?)","page"', html)
            for i in range(0, len(lists)):
                lists[i] = lists[i].replace("\\", '')
            try:
                os.mkdir(doc_id)
            except:
                pass
            for i in range(0, len(lists)):
                img = requests.get(lists[i]).content
                with open(doc_id+'\img'+str(i)+'.jpg', 'wb') as m:
                    m.write(img)
            lb.insert(END, "FPD图片保存在" + doc_id + "文件夹\n")
            lb.see(END)
            get_success("FPD图片保存在" + doc_id + "文件夹")

        def thread_it(func, *args):
            '''将函数打包进线程'''
            # 创建
            t = threading.Thread(target=func, args=args)
            # 守护 !!!
            t.setDaemon(True)
            # 启动
            t.start()
            # 阻塞--卡死界面！
            # t.join()
        b_type = b_input_type.get()
        file_url = b_url.get()

        if file_url == "":
            lb.insert(END, "错误：请填写文档地址！\n")
            lb.see(END)
        elif b_type == "":
            lb.insert(END, "错误：请选择文档类型！\n")
            lb.see(END)
        else:
            lb.insert(END, "文档地址：" + file_url + "\n")
            lb.insert(END, "类型：" + b_type+"\n")
            lb.insert(END, "爬取中.."+"\n")
            lb.see(END)
            thread_it(eval(b_type.upper())(file_url))
    # 创建顶层窗口
    win = tkinter.Tk()
    # 设置窗口大小
    win.geometry('320x400')
    # 设置窗口标题
    win.title('百度文档爬虫-by Hokoa')
    # 禁止调整窗口大小
    win.resizable(0, 0)
    label_tips = tkinter.Label(win, text='PDF|PPT只能下载图片,如下载不成功请尝试更换类型\n示例地址：https://wenku.baidu.com/view/6c3a567e2dc58bd63186bceb19e8b8f67d1cef5e.html',
                               fg='#ff6600', font='YaHei 9', wraplength=280, justify='left')
    label_tips.place(x=20, y=20)
    # 链接
    label_url = tkinter.Label(win, text='链接:', font='YaHei 9', fg='green')
    label_url.place(x=20, y=70)
    # 链接输入框
    b_url = tkinter.StringVar()
    b_input_url = tkinter.Entry(win, textvariable=b_url)
    b_input_url.place(x=80, y=70)
    # 类型
    label_type = tkinter.Label(win, text='类型:', font='YaHei 9', fg='green')
    label_type.place(x=20, y=100)
    # 类型选择框
    b_input_type = ttk.Combobox(win)
    b_input_type['value'] = ('DOC', 'PPT', 'TXT', 'PDF')
    b_input_type.current(2)
    b_input_type.place(x=80, y=100)

    # 信息提示

    loginfo = tkinter.Frame(win)
    loginfo.place(x=20, y=135)
    sb = tkinter.Scrollbar(loginfo)
    sb.pack(side=RIGHT, fill=Y)
    lb = tkinter.Text(loginfo,  yscrollcommand=sb.set, height=15, width=38)
    lb.pack(side=RIGHT, fill=Y)
    sb.config(command=lb.yview)

    # 创建一个装按钮的容器
    panel = tkinter.Frame(win)
    # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定事件回调函数
    button_getimg = tkinter.Button(
        panel, text='开始抓取', command=run_start)
    button_getimg.pack(side='left', padx="20")
    button_quit = tkinter.Button(panel, text='退出', command=confirm_to_quit)
    button_quit.pack(side='right', padx="20")
    panel.pack(side='bottom', pady="20")
    # 开启主事件循环
    tkinter.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        lb.insert(END, "获取出错，可能URL错误")
        lb.see(END)
        print("获取出错，可能URL错误")
