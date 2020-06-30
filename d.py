import requests
import re
import argparse
import sys
import json
import os


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


def main():

    # 抓取前验证

    # def get_before_check():
    #     keyword = b_url.get()  # 抓取百度文档的关键字
    #     img_num = b_num.get()  # 要抓取的图片数量
    #     addr = b_addr.get()  # 图片保存路径
    #     if img_num == "":
    #         color, msg = ('red', '抓取数量不能为空')
    #         label_info.config(text=msg, fg=color)
    #     elif addr == "":
    #         color, msg = ('red', '请选择保存路径')
    #         label_info.config(text=msg, fg=color)
    #     else:
    #         color, msg = ('orange', '抓取中....')
    #         label_info.config(text=msg, fg=color)
    #         # time.sleep(5)
    #         get_img(keyword, img_num, addr)

    def confirm_to_quit():
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
            win.quit()
    # 选择保存路径

    def select_dir():
        save_path = askdirectory()
        b_addr.set(save_path)  # 获取输入框内容

    def run_start():
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
                # print("文档保存在"+filename)

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
            # print("PPT图片保存在" + doc_id + "文件夹")

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
            # print(texts)
            filename = doc_id+'.txt'
            with open(filename, 'a', encoding='utf-8') as f:
                for i in range(0, len(texts)):
                    texts[i] = texts[i].replace('\\r', '\r')
                    texts[i] = texts[i].replace('\\n', '\n')

                    f.write(texts[i])
            lb.insert(END, "\n"+"文档保存在" + filename+"\n")
            # print("文档保存在" + filename)

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
            # print("FPD图片保存在" + doc_id + "文件夹")

        b_type = b_input_type.get()
        file_url = b_url.get()
        # file_addr = b_addr.get()

        if file_url == "":
            lb.insert(END, "错误：请填写文档地址！\n")
        elif b_type == "":
            lb.insert(END, "错误：请选择文档类型！\n")
        # elif file_addr == "":
        #     lb.insert(END, "错误：请选择保存地址！\n")
        else:
            lb.insert(END, "文档地址：" + file_url + "\n")
            lb.insert(END, "类型：" + b_type+"\n")
            lb.insert(END, "保存地址" + file_addr+"\n")
            lb.insert(END, "爬取中.."+"\n")
            eval(b_type.upper())(file_url)
    # 创建顶层窗口
    win = tkinter.Tk()
    # 设置窗口大小
    win.geometry('320x400')
    # 设置窗口标题
    win.title('百度文档爬虫-by Hokoa')
    # 禁止调整窗口大小
    win.resizable(0, 0)

    label_tips = tkinter.Label(
        win, text='PDF|PPT只能下载图片,如下载不成功请尝试更换类型', font='YaHei 9', fg='#ff6600')
    label_tips.place(x=20, y=20)
    # 链接
    label_url = tkinter.Label(win, text='链接:', font='YaHei 9', fg='green')
    label_url.place(x=20, y=50)
    # 链接输入框
    b_url = tkinter.StringVar()
    b_input_url = tkinter.Entry(win, textvariable=b_url)
    b_input_url.place(x=80, y=50)

    # 类型
    label_type = tkinter.Label(win, text='类型:', font='YaHei 9', fg='green')
    label_type.place(x=20, y=80)
    # 类型选择框
    b_input_type = ttk.Combobox(win)
    b_input_type['value'] = ('DOC', 'PPT', 'TXT', 'PDF')
    b_input_type.current(2)
    b_input_type.place(x=80, y=80)

    # # 保存路径
    # label_addr = tkinter.Label(win, text='保存地址：', font='YaHei 9', fg='green')
    # label_addr.place(x=20, y=110)
    # # 保存路径输入框
    # b_addr = tkinter.StringVar()
    # b_input_addr = tkinter.Entry(win, textvariable=b_addr, state='readonly')
    # b_input_addr.place(x=80, y=110)
    # # 选择路径按钮
    # button_addr = tkinter.Button(win, text='选择', command=select_dir)
    # button_addr.place(x=230, y=105)

    # 信息提示

    loginfo = tkinter.Frame(win)
    loginfo.place(x=20, y=105)
    sb = tkinter.Scrollbar(loginfo)
    sb.pack(side=RIGHT, fill=Y)
    lb = tkinter.Text(loginfo,  yscrollcommand=sb.set, height=15, width=38)
    lb.pack(side=RIGHT, fill=Y)
    sb.config(command=lb.yview)
    # label_info = tkinter.Scrollbar(win, text='未开始', font='YaHei 9', fg='red')
    # label_info.place(x=20, y=140)

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
    except:
        lb.insert(END, "获取出错，可能URL错误\n使用格式name.exe url type\n请使用--help查看帮助")
        print("获取出错，可能URL错误\n使用格式name.exe url type\n请使用--help查看帮助")
