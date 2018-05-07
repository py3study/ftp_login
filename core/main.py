import sys
from conf import settings
from core.login import Login
from core.client import Client
from lib.Prompt import Prompt


def main():
    ret = Login().login()  # 执行登录程序,返回字典
    if ret:
        clas = getattr(sys.modules['core.client'], 'Client')  # 根据角色名获取类名(角色名和类名一致)
        obj = clas(ret)
        obj.main()  # 执行主菜单
