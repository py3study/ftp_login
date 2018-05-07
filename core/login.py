from conf import settings
from lib.mylogger import Logger
from lib.mypickle import MyPickle
from lib.Prompt import Prompt
from core.client import Client


class Login(object):  # 用户登录
    def __init__(self):
        self.auth_dic = {'username': None,  # 用户名
                         'status': False,  # 登录状态
                         'color': None,  # 用户角色
                         'failures': 1,  # 失败次数
                         'maximum': 3,  # 最大登录次数
                         'flag': True,  # 标志位,判断退出首页菜单
                         }

    '''装饰器用于验证是否登录'''

    def wrapper(func):
        def inner(self):
            if self.auth_dic['status']:
                ret = func(self)
                return ret
            else:
                print('|| 请先进行登录!')
                if self.login():
                    ret = func(self)
                    return ret

        return inner

    def login(self):
        # 判断失败次数是否小于等于最大失败次数
        while self.auth_dic['failures'] <= self.auth_dic['maximum']:
            username = input('请输入登录用户名: ').strip()
            if not username:
                print(Prompt.display('用户名不能为空!', 'red'))
                continue
            password = input('请输入登录密码: ').strip()
            if not password:
                print(Prompt.display('密码不能为空!', 'red'))
                continue

            # 判断用户名和密码是否一致
            res = Client('').login_auth(username, password)

            if res:
                print(Prompt.display('登陆成功!', 'green'))
                Logger.logger.info('%s 登陆成功' % username)
                # 修改初始变量
                self.auth_dic['username'] = username
                self.auth_dic['status'] = True
                # self.auth_dic['color'] = res['color']
                # return {'username': username, 'color': res['color']}  # 返回字典给调用者
                return username
            else:
                chance = self.auth_dic['maximum'] - self.auth_dic['failures']  # 剩余失败次数
                print(Prompt.display('用户或密码错误,请重新输入!您还有%s次机会!' % chance, 'red'))
                self.auth_dic['failures'] += 1  # 失败次数加1
                Logger.logger.info('%s 登陆失败%s次' % (username, self.auth_dic['maximum'] - chance))

            # 判断失败次数大于最大次数时，直接退出!
            if self.auth_dic['failures'] > self.auth_dic['maximum']:
                self.auth_dic['flag'] = False
                return False

    @staticmethod
    def user_auth(username, password):
        '''
        #判断用户名和密码是否匹配
        :param username: 用户名
        :param password: 密码
        :return: True 匹配成功 False 匹配失败
        '''
        if not username or not password:
            print(Prompt.display('用户名或者密码不能为空!', 'red'))
            return False

        # user = MyPickle(settings.file_name['user'])
        # read_user = user.load()
        # for i in read_user:
        #     if username == i['username'] and password == i['password']:
        #         result = {'msg': True, 'color': i['color']}
        #         return result
        # else:
        #     return {'msg': False, 'color': None}


# def get_pwd(username, password):  # 用于别的模块导入
#     return Login().get_pwd(username, password)


if __name__ == '__main__':
    Login().login()
