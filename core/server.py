import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))  # 添加项目根目录到系统环境变量
import socket
import hashlib
from conf import settings
from lib.mypickle import MyPickle

user_list = [
    {'username': 'xiao', 'password': '123'},
    {'username': 'zhangsan', 'password': '123'},
    {'username': 'lisi', 'password': '123'},
]


class Server(object):
    # action_list = [
    #     ('登录', 'login'),
    #     ('创建目录', 'create_directory'),
    #     ('退出', 'q'),
    # ]

    def __init__(self):
        self.ip = settings.server['ip']
        self.port = settings.server['port']
        self.max = settings.server['rxb']  # 最大接收1024字节
        self.user_files = MyPickle(settings.file_name['user'])
        self.base_dir = os.path.dirname(os.getcwd())
        self.action_list = [
            ('login', self.login),
            ('create_directory', self.create_directory),
            #('q', self.q),
        ]

    def main(self):
        sk = socket.socket()  # 创建套接字
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口复用
        sk.bind((self.ip, self.port))  # 把地址绑定到套接字
        sk.listen()  # 监听连接

        while True:
            conn, addr = sk.accept()  # 等待接受客户端连接
            msg = conn.recv(self.max).decode('utf-8')  # 接收的信息解码
            print('收到一条消息:%s' % msg)

            if msg.upper() == 'Q':  # 判断接收的信息是否为q
                conn.close()  # 关闭客户端套接字
                #sk.close()  # 关闭服务器套接字,不再接收请求
                break  # 退出while循环

            handle, info = msg.split('!')  # 操作类型,数据

            ret = self.action(handle, info)
            conn.send(str(ret).encode('utf-8'))  # 布尔值需要转化为str

        sk.close()


    @staticmethod
    def second_encrypt(username, password):
        if not username or not password:
            return '用户名和密码不能为空!'

        salt = settings.secret_key['second']  # 第二层密码盐

        m = hashlib.md5((username + salt).encode('utf-8'))  # 双层密码盐(用户名和密码盐组合)
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    def action(self, handle, info):  # 动作判断
        if not handle:
            return '操作名不能为空'

        for i in self.action_list:
            if i[0] == handle:
                #print(i[1])
                #print(info)
                return i[1](info)  # 执行对应的动作

        else:
            return False

    def login(self, info):
        if not info:
            return '用户名信息不能为空'

        username, password = info.split(':')  # 获取第一次加密密码
        second = self.second_encrypt(username, password)  # 第二层加密

        for i in self.user_files.load():
            if i['username'] == username and i['password'] == second:
                return True

        return False

    def create_directory(self,name):  # 创建目录,路径是以home为基准
        new_dir = self.base_dir+r'\home\{}'.format(name)
        #print(new_dir)
        try:
            if os.path.exists(new_dir):
                return False
            else:
                os.mkdir(new_dir)
                return True
        except Exception as e:
            print(e)
            return False





def second_encrypt(username, password):  # 用于别的模块导入
    return Server().second_encrypt(username, password)


if __name__ == '__main__':
    Server().main()
    #ret = Server().create_directory('xiao')
    #print(ret)
