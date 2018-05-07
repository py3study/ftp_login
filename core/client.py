import socket
import hashlib
from conf import settings
from lib.Prompt import Prompt


class Client(object):
    def __init__(self, username):
        self.ip = settings.server['ip']
        self.port = settings.server['port']
        self.max = settings.server['rxb']
        # self.token = token
        self.username = username
        self.operate_lst = [
            ('查看文件', self.see_file),
            ('上传文件', self.upload_file),
            ('下载文件', self.download_file),
            ('删除文件', self.delete_files),
            ('退出', self.q),
        ]

    def main(self):
        print(Prompt.display('您好: {} 欢迎使用聊天系统!\n'.format(self.username), 'purple_red'))
        self.menu()

    def menu(self):
        while True:
            self.interlacing_color(self.operate_lst)  # 隔行换色
            num = input('输入您要做的操作序号：').strip()
            if num.isdigit():  # 判断数字
                num = int(num)  # 转换数字类型
                if num in range(1, len(self.operate_lst) + 1):  # 判断输入的序号范围
                    # print(operate_lst[num - 1][0])
                    self.operate_lst[num - 1][1]()
                else:
                    print('序号不存在,请重新输入!')
            else:
                print('操作序号必须为数字!')

    def see_file(self):
        print(Prompt.display('功能未实现,敬请期待!', 'green'))

    def upload_file(self):
        print(Prompt.display('功能未实现,敬请期待!', 'green'))

    def download_file(self):
        print(Prompt.display('功能未实现,敬请期待!', 'green'))

    def delete_files(self):
        print(Prompt.display('功能未实现,敬请期待!', 'green'))

    def q(self):
        self.send_info('q')
        exit()

    def send_info(self,msg):
        sk = socket.socket()  # 创建客户套接字
        sk.connect((self.ip, self.port))  # 尝试连接服务器
        sk.send(msg.encode('utf-8'))
        ret = sk.recv(1024).decode('utf-8')
        sk.close()
        return ret

    def login_auth(self, username, password):
        # sk = socket.socket()  # 创建客户套接字
        # sk.connect((self.ip, self.port))  # 尝试连接服务器
        # encrypt_pwd = self.get_pwd(username, password)  # 第一层加密
        # msg = '{}!{}'.format('login', username + ':' + encrypt_pwd)
        # sk.send(msg.encode('utf-8'))
        # ret = sk.recv(1024).decode('utf-8')
        #
        # if ret == 'True':
        #     return True
        # else:
        #     return False
        #
        # sk.close()
        encrypt_pwd = self.get_pwd(username, password)  # 第一层加密
        msg = '{}!{}'.format('login', username + ':' + encrypt_pwd)
        ret = self.send_info(msg)
        if ret == 'True':
            self.send_info('{}!{}'.format('create_directory',username))  # 自动创建用户目录
            #print(ret1)
            return True
        else:
            return False

    @staticmethod
    def get_pwd(username, password):
        '''
        获取加密密码
        :param username: 用户名
        :param password: 密码
        :return: 32位的十六进制数据字符串
        '''
        if not username or not password:
            return '用户名和密码不能为空!'

        salt = settings.secret_key['first']  # 第一层密码盐
        # print()
        m = hashlib.md5((username + salt).encode('utf-8'))  # 双层密码盐(用户名和密码盐组合)
        m.update(password.encode('utf-8'))
        return m.hexdigest()

    def interlacing_color(self, custom_list):  # 列表隔行换色
        diff = 0  # 差值
        if len(custom_list) > len(Prompt.colour_dic):  # 当菜单列表长度大于颜色列表长度时
            diff = len(custom_list) - len(Prompt.colour_list)  # 菜单列表长度-颜色列表长度

        colour_list = list(Prompt.colour_dic)
        new_list = colour_list  # 新的颜色列表

        if diff >= 0:  # 当菜单列表长度大于等于颜色列表长度时
            for i in range(diff + 1):
                new_list.append(colour_list[i])  # 添加颜色,使颜色列表等于菜单列表长度

        count = -1  # 颜色列表索引值，默认为-1
        for key, item in enumerate(custom_list, 1):  # 获取每个角色类的operate_lst静态属性,显示的序列号从1开始
            count += 1  # 索引加1
            if type(item) == str:
                ret = Prompt.random_color('{}.\t{}'.format(key, item))  # 随机显示颜色
                print(ret)
            else:
                length = len(item)
                if length == 2:
                    ret = Prompt.display('{}.\t{}'.format(key, item[0]), new_list[count])  # 按照列表顺序显示颜色
                    print(ret)
                elif length == 5:
                    ret = Prompt.display('{}.\t{}'.format(key, item['username']), item['color'])  # 按照列表顺序显示颜色
                    print(ret)


def get_pwd(username, password):  # 用于别的模块导入
    return Client().get_pwd(username, password)


if __name__ == '__main__':
    Client().main()
