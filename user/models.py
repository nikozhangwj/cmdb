# encoding: utf-8

import json

from django.db import models

import MySQLdb as mysqldb
from MySQLdb import cursors
# Create your models here.


# 用户信息文件路径
path = 'user.data.json'

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "dfl^!G321"
MYSQL_DB = "cmdb_niko"
MYSQL_CHARSET = "utf8"
SQL_LOGIN = '''
                SELECT id,name,age,tel,sex
                FROM user
                WHERE name=%s and password=%s LIMIT 1;
            '''

SQL_LIST = '''
                SELECT id,name,age,tel,sex
                FROM user
            '''

SQL_USER = '''
                SELECT id,name,age,tel,sex
                FROM user
                WHERE id=%s
            '''

SQL_USER_BY_NAME = '''
                SELECT id,name,age,tel,sex
                FROM user
                WHERE name=%s
            '''
SQL_UPDATE_USER = '''
                UPDATE user SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s
            '''

SQL_CREATE_USER = '''
                INSERT INTO user(name,age,tel,sex,password) VALUES(%s, %s, %s, %s, %s)     
                '''

# 获取用户信息并序列化
def get_users():
    conn = mysqldb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_LIST)
    users = cur.fetchall()
    #print(users)
    cur.close()
    conn.close()
    return users


def get_user(uid):
    conn = mysqldb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_USER,(str(uid),))
    user = cur.fetchall()
    cur.close()
    conn.close()
    return user


def save_user(users):
    fhandler = open(path,'wt')
    user = json.dumps(users)
    fhandler.write(user)
    fhandler.close()
    return True


# 验证登陆信息
def valid_login(username,password):
    conn = mysqldb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor()
    cur.execute(SQL_LOGIN,(username,password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    print("login")
    return {'id':result[0],'name':result[1]} if result else None

#通过回传的uid删除用户
def delete_user(uid):
    users = get_users()
    users.pop(uid,None)
    save_user(users)
    return True

def get_user_byname(name):
    conn = mysqldb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_USER_BY_NAME,(name,))
    user = cur.fetchall()
    #print(user)
    cur.close()
    conn.close()
    return user

def vaild_name_unique(name,uid):
    user = get_user_byname(name)
    if user is None:
        return True
    else:
        return str(user[0]['id']) == str(uid)


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
    if get_user(user['id']) is None:
        error['id'] = '用户数据无效'
        is_valid = False

    #检查用户名是否存在
    user['name'] = username.strip()
    if not vaild_name_unique(user['name'],user['id']):
        is_valid = False
        error['name'] = '用户名已存在'


    #检查年龄格式是否正确
    user['age'] = age.strip()
    if not user['age'].isdigit():
        error['age'] = '年龄格式错误'
        is_valid = False

    user['tel'] = tel.strip()
    user['sex'] = int(sex)
    #print(user)
    return user,is_valid,error

#把用户信息update到数据文件中
def update_user(user):
    #print(user)
    conn = mysqldb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor()
    cur.execute(SQL_UPDATE_USER,(user['name'],user['age'],user['tel'],user['sex'],user['id']))
    conn.commit()
    cur.close()
    conn.close()
    return True


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
        if get_user_byname(user['name']):
                is_valid = False
                error['name'] = '用户名已存在'

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
    print(user)
    conn = mysqldb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor()
    cur.execute(SQL_CREATE_USER,(user['name'],user['age'],user['tel'],user['sex'],user['password']))
    conn.commit()
    cur.close()
    conn.close()
    return True

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
