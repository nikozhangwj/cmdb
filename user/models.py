# encoding: utf-8

import json

from django.db import models

# Create your models here.


# 用户信息文件路径
path = 'user.data.json'


# 获取用户信息并序列化
def get_user():
    fhandler = open(path,'rt')
    users = json.loads(fhandler.read())
    fhandler.close()
    return users


# 验证登陆信息
def valid_login(username,password):
    users = get_user()
    for key,user in users.items():
        if username == user['name'] and password == user['password']:
            user['id'] = key
            return user
    return False