# encoding: utf-8

import json

from django.db import models

# Create your models here.


# 用户信息文件路径
path = 'user.data.json'


# 获取用户信息并序列化
def get_users():
    fhandler = open(path,'rt')
    users = json.loads(fhandler.read())
    fhandler.close()
    return users


def get_user(uid):
    user = get_users().get(uid,{})
    user['id'] = uid
    return user


def save_user(users):
    fhandler = open(path,'wt')
    user = json.dumps(users)
    fhandler.write(user)
    fhandler.close()
    return True


# 验证登陆信息
def valid_login(username,password):
    users = get_users()
    for key,user in users.items():
        if username == user['name'] and password == user['password']:
            user['id'] = key
            return user
    return False


def delete_user(uid):
    users = get_users()
    users.pop(uid,None)
    save_user(users)
    return True


def valid_update_user(params):
    #从参数获取前端数据
    uid = params.get('uid')
    username = params.get('username')
    age = params.get('age')
    sex = params.get('sex')
    tel = params.get('tel')
    #从 get_users()函数获取用户数据
    users = get_users()
    #初始化函数内变量
    user = {}
    error = {}
    is_valid = True
    #检查用户是否有效
    user['id'] = uid.strip()
    if not users.get(user['id']):
        error['id'] = '用户数据无效'
        is_valid = False

    #检查用户名是否存在
    user['name'] = username.strip()
    for key,value in users.items():
        if user['name'] == value.get('name') and uid != key:
            is_valid = False
            error['name'] = '用户名已存在'

    #检查年龄格式是否正确
    user['age'] = age.strip()
    if not user['age'].isdigit():
        error['age'] = '年龄格式错误'
        is_valid = False

    user['tel'] = tel.strip()
    user['sex'] = int(sex)

    return user,is_valid,error


def update_user(user):
    users = get_users()
    uid = user.pop('id')
    users[uid].update(user)
    return save_user(users)