file_name = {
    'user': '../db/user_info.txt',  # 用户名和密码验证文件
    'log_path': '../log/test.log',  # 日志文件
}

server = {  # 服务器信息
    'ip': '127.0.0.1',
    'port': 9090,
    'rxb': 1024,
}

secret_key = {
    'first': '༺ཌ༈༒༈ད༻'.encode('utf-8').decode('utf-8'),  # 第一层加密盐
    'second': '༺༽༾ཊ࿈ཏ༿༼༻'.encode('utf-8').decode('utf-8'),  # 第二层密码盐
    'token_salt': '❀༒❀'.encode('utf-8').decode('utf-8'),  # token加密盐
}
