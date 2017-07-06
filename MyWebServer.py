#coding : utf-8
from multiprocessing import Process

import socket
import sys
import re


#print( request_data.decode("utf-8"))
#client.send("recerve from s%" % addr)
root='C:\python34\MyWebServer'

class HTTPServer(object):
    ''''''
    def __init__(self,application):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.app = application


    def bind(self,port):
        self.server.bind(('',port))

    def start(self):
        self.server.listen(128)                   #开启监听
        while True:                             #当有客户端连接，开启一个进程处理
            client,addr=self.server.accept()
            http_process=Process(target=self.client_handler,args=(client,))
            http_process.start()
            client.close()                        #开启进程时复制了一份客户端套接字，所以这边要关闭

    def start_response(self,status,headers):      #构造响应头
        '''
        status
        headers=[
            ('','')
        ]
        '''
        response_headers = "HTTP/1.1 " + status + "\r\n"
        for header in headers:
             response_headers += "%s: %s\r\n" % header
        self.response_headers = response_headers

    def client_handler(self,client):                #具体的处理函数
        request_data = client.recv(1024)            #获取请求信息，分析提取请求头
        request_lines = request_data.splitlines()
        method_filename = re.search(r'\w+ +(/[^ ]*) ', request_lines[0].decode("utf-8")).group(0).split(' ')
        #print(method_filename)
        filename = method_filename[1]
        method = method_filename[0]

        print(method)

        #if filename.endswith('.py'):
        #   m = __import__(filename[1:-3])
        env={                                         #将请求信息存储为字典，传入应用，获取响应头+响应主体，将响应回传客户端
                "PATH_INFO":filename,
                "METHOD": method
        }
        response_body = self.app(env, self.start_response)

        response = self.response_headers + '\r\n' + response_body
        client.send(bytes(response,'utf-8'))
        client.close()

def main():
    sys.path.insert(1,root)
    if len(sys.argv) < 2:
        sys.exit("python MyWebServer WebFramework:app")
    moudle_name,app_name=sys.argv[1].split(":")
    #在服务器开启时，设置响应包及其中应用
    #类似 python MyWebServer WebFramework : Application
    m = __import__(moudle_name)
    application= getattr(m,app_name)
    http_server = HTTPServer(application)
    http_server.bind(8000)
    http_server.start()


if __name__ =="__main__":
    main()







