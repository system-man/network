#coding:utf-8

import time

root='.'

class Application(object):
    '''构造应用'''
    def __init__(self,urls):
        self.urls=urls

    def __call__(self,env,start_response):
        path = env.get("PATH_INFO","/")
        if path.startswith("/static"):
            filename = path[8:]                   #如果是get 静态文件，获取文件名，打开读取内容
            try:
                f=open(root + filename, 'rb')
            except IOError:                      #未能打开，则返回404，not found
                status="404 Not Found"
                headers=[]
                start_response(status,headers)
                return "Not found"
            else:
                file = f.read()
                f.close()

                #构造成功的响应头
                status="200 OK"
                headers=[]
                start_response(status,headers)
                return file.decode("utf-8")

        for url,handler in self.urls:    #非get 静态文件时，根据url判断处理函数，进而构造响应头+主体
            if path == url:
               return handler(env,start_response)

def show_time(env,start_response):
    status="200 OK"
    headers=[
        ("Content-Type","text/plain")
    ]
    start_response(status,headers)
    return time.ctime()


def say_hello(env,start_response):
    status = "200 OK"
    headers = [
        ("Content-Type", "text/plain")
    ]
    start_response(status, headers)
    return "say hello!"


urls=[
    ("/showtime",show_time),
    ("/sayhello",say_hello),
]


app = Application(urls)    #这是一个单例模式
