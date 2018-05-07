# -*- coding: utf-8 -*-
# 自动创建settings模块中的所有txt文件
# 不存在则创建,否则不创建

import os
from conf import settings
from lib.mypickle import MyPickle
from core.client import get_pwd
from core.server import second_encrypt

files = settings.file_name  # 获取文件字典
for i in files:  # 遍历字典
    if os.path.exists(settings.file_name[i]) is False:  # 判断文件是否存在，False表示不存在
        with open(settings.file_name[i], mode='ab') as mk:  # 打开每一个文件
            if i == 'user':  # 判断是否为用户认证文件
                # 写入默认的用户认证文件
                user_list = [('xiao', '123')]
                for j in user_list:
                    info = {}

                    encrypt_pwd = get_pwd(j[0], j[1])  # 第一层加密
                    second = second_encrypt(j[0], encrypt_pwd)  # 第二层加密
                    # exit()
                    # token =

                    info = {'username': j[0], 'password': second}
                    MyPickle(files[i]).dump(info)  # 写入文件
