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

#通过回传的uid删除用户
def delete_user(uid):
    users = get_users()
    users.pop(uid,None)
    save_user(users)
    return True

#update功能预检查数据
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
            break

    #检查年龄格式是否正确
    user['age'] = age.strip()
    if not user['age'].isdigit():
        error['age'] = '年龄格式错误'
        is_valid = False

    user['tel'] = tel.strip()
    user['sex'] = int(sex)

    return user,is_valid,error

#把用户信息update到数据文件中
def update_user(user):
    users = get_users()
    uid = user.pop('id')
    users[uid].update(user)
    return save_user(users)


#验证创建用户信息
def valid_create_user(params):
    name = params.get('username','')
    age = params.get('age','0')
    sex = params.get('sex','0')
    tel = params.get('tel','')
    password1 = params.get('password1')
    password2 = params.get('password2')
    users = get_users()
    #uid = int(sorted(users.items(),key=lambda x:x[0],reverse=True)[0][0]) + 1

    is_valid = True
    user = {}
    error = {}

    user['name'] = name.strip()
    if user['name'] == '':
        is_valid = False
        error['name'] = '名字不能为空'
    else:
        for key,value in users.items():
            if user['name'] == value.get('name'):
                is_valid = False
                error['name'] = '用户名已存在'
                break

    user['age'] = age.strip()
    if not user['age'].isdigit():
        is_valid = False
        error['age'] = '年龄格式错误'

    user['sex'] = sex
    user['tel'] = tel
    user['password'] = password1.strip()
    if user['password'] == '' or user['password'] != password2.strip():
        is_valid = False
        error['password'] = '密码不能为空或两次输入不同'

    return is_valid,user,error


def create_user(user):
    users = get_users()
    uid = max([int(key) for key in users]) + 1
    users[uid] = user
    return save_user(users)


def valid_cp(params,param):
    old_password = params.get('old_password')
    new1_password = params.get('new1_password')
    new2_password = params.get('new2_password')
    uid = param.get('user')['id']

    errors = {}
    is_valid = True
    users = get_users()
    user_password = users[uid]['password']

    if old_password.strip() == '':
        is_valid = False
        errors['old_password'] = '密码不能为空'

    if old_password.strip() != user_password:
        is_valid = False
        errors['old_password'] = '你输入的密码不正确'

    if new1_password.strip() != new2_password.strip() or new1_password.strip() == '':
        is_valid = False
        errors['new_password'] = '密码不能为空或两次输入不同'

    return is_valid,new1_password,uid,errors


def cp(uid,new_password):
    users = get_users()
    users[uid]['password'] = new_password
    return save_user(users)
