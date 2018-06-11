# encoding: utf-8

from django.db import models
# 导入模块
import MySQLdb as mysqldb
from MySQLdb import cursors
from .dbutils import mysql_connection
# Create your models here.






class User(object):
    SQL_USER_PASSWORD = '''
                SELECT password
                FROM user
                WHERE id=%s
                '''
    SQL_CHANGE_PASSWORD = '''
                UPDATE user SET password=%s WHERE id=%s
            '''
    SQL_CREATE_USER = '''
                INSERT INTO user(name,age,tel,sex,password) VALUES(%s, %s, %s, %s, %s)
                '''
    SQL_UPDATE_USER = '''
                UPDATE user SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s
            '''
    SQL_USER_BY_NAME = '''
                SELECT id,name,age,tel,sex
                FROM user
                WHERE name=%s
            '''
    SQL_DELETE_USER ='''
                DELETE FROM user WHERE id=%s
                '''
    SQL_USER = '''
                SELECT id,name,age,tel,sex
                FROM user
                WHERE id=%s
            '''
    SQL_LIST = '''
                SELECT id,name,age,tel,sex
                FROM user
            '''
    SQL_LOGIN = '''
                SELECT id,name,age,tel,sex,password
                FROM user
                WHERE name=%s and password=%s LIMIT 1;
            '''

    def __init__(self, id=None, name='', age=0, tel='', sex=1, password=''):
        self.id = id
        self.name = name
        self.age = age
        self.tel = tel
        self.sex = sex
        self.password = password

    @classmethod
    def valid_login(cls,name,password):
        args = (name,password)
        cnt, result = mysql_connection.mysql_ut(cls.SQL_LOGIN,(name,password),one=True)
        if result:
            return User(id=result[0],name=result[1],age=result[2],tel=result[3],sex=result[4],password=result[5])
        else:
            return None

    @classmethod
    def get_list(cls):
        cnt,result = mysql_connection.mysql_ut(cls.SQL_LIST)
        return [User(id=line[0],name=line[1],age=line[2],tel=line[3],sex=line[4]) for line in result]

    @classmethod
    def get_user_by_id(cls,uid):
        cnt,result = mysql_connection.mysql_ut(cls.SQL_USER,(str(uid),),one=True)
        #print(result)
        return User(id=result[0],name=result[1],age=result[2],tel=result[3],sex=result[4])

    @classmethod
    def get_user_by_name(cls,name):
        cnt,result = mysql_connection.mysql_ut(cls.SQL_USER_BY_NAME,(name,),one=True)
        #print(result)
        return User(id=result[0],name=result[1],age=result[2],tel=result[3],sex=result[4]) if result else None

    @classmethod
    def delete_user(cls,uid):
        cnt,result = mysql_connection.mysql_ut(cls.SQL_DELETE_USER,(str(uid),),fetch=False)
        return True

    @classmethod
    def vaild_name_unique(cls,name,uid):
        user = cls.get_user_by_name(name)
        #print(user)
        if not user:
            return True
        else:
            return str(user.id) == str(uid)

    @classmethod
    def valid_update_user(cls,params):
        #初始化函数内变量
        user = User()
        error = {}
        is_valid = True
        #检查用户是否有效
        user.id = params.get('uid').strip()
        if cls.get_user_by_id(user.id) is None:
            error['id'] = '用户数据无效'
            is_valid = False

        #检查用户名是否存在
        user.name = params.get('username').strip()
        if not cls.vaild_name_unique(user.name,user.id):
            is_valid = False
            error['name'] = '用户名已存在'

        #检查年龄格式是否正确
        user.age = params.get('age').strip()
        if not user.age.isdigit():
            error['age'] = '年龄格式错误'
            is_valid = False

        user.tel = params.get('tel').strip()
        user.sex = int(params.get('sex'))
        #print(user)
        return user,is_valid,error

    def update_user(self):
        #print(user)
        args = (self.name,self.age,self.tel,self.sex,self.id)
        cnt,result = mysql_connection.mysql_ut(self.SQL_UPDATE_USER,args,fetch=False)
        return True

    def as_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'age' : self.age,
            'tel' : self.tel,
            'sex' : self.sex,
            'password' : self.password
        }

    @classmethod
    def valid_create_user(cls,params):
        is_valid = True
        user = User()
        error = {}

        user.name = params.get('username','').strip()
        if user.name == '':
            is_valid = False
            error['name'] = '名字不能为空'
        else:
            if cls.get_user_by_name(user.name):
                    is_valid = False
                    error['name'] = '用户名已存在'

        user.age = params.get('age','0').strip()
        if not user.age.isdigit():
            is_valid = False
            error['age'] = '年龄格式错误'

        user.sex = params.get('sex','0')
        user.tel = params.get('tel','')
        user.password = params.get('password1').strip()
        if user.password == '' or user.password != params.get('password2').strip():
            is_valid = False
            error['password'] = '密码不能为空或两次输入不同'
        #print(user.name,user.age,user.sex,user.tel,user.password)
        return is_valid,user,error

    def create_user(self):
        #print(user)
        args = (self.name,self.age,self.tel,self.sex,self.password)
        cnt,result = mysql_connection.mysql_ut(self.SQL_CREATE_USER,args,fetch=False)
        return True

    @classmethod
    def get_user_password(cls,uid):
        cnt,user = mysql_connection.mysql_ut(cls.SQL_USER_PASSWORD,(str(uid),))
        return user

    @classmethod
    def valid_cp(cls,params,param):
        errors = {}
        is_valid = True

        if params.get('old_password').strip() == '':
            is_valid = False
            errors['old_password'] = '密码不能为空'

        if params.get('old_password').strip() != get_user_password(param.get('user')['id'])[0].get('password'):
            is_valid = False
            errors['old_password'] = '你输入的密码不正确'

        if params.get('new1_password').strip() != params.get('new2_password').strip() or params.get('new1_password').strip() == '':
            is_valid = False
            errors['new_password'] = '密码不能为空或两次输入不同'

        return is_valid,params.get('new1_password').strip(),param.get('user')['id'],errors


    def cp(self,uid,new_password):
        cnt,result = mysql_connection.mysql_ut(self.SQL_CHANGE_PASSWORD,(new_password,uid),fetch=False)
        return True




# 获取所有用户信息并序列化
def get_users():
    cnt,result = mysql_connection.mysql_ut(SQL_LIST)
    users = result
    return users

# 通过uid获取单个用户信息并序列化
def get_user(uid):
    cnt,result = mysql_connection.mysql_ut(SQL_USER,(str(uid),))
    user = result
    return user


# 验证登陆信息
def valid_login(username,password):
    cnt,result = mysql_connection.mysql_ut(SQL_LOGIN,(username,password),one=True)
    #print('ID: ',result.get('id'),'NAME: ',result.get('name'),"login")
    return {'id':result.get('id'),'name':result.get('name')} if result else None


# 通过回传的uid删除用户
def delete_user(uid):
    cnt,result = mysql_connection.mysql_ut(SQL_DELETE_USER,(str(uid),),fetch=False)
    return True

# 通过用户name获取用户信息
def get_user_byname(name):
    cnt,result = mysql_connection.mysql_ut(SQL_USER_BY_NAME,(name,))
    user = result
    print(user)
    return user

# 判断应户名是否唯一
def vaild_name_unique(name,uid):
    user = get_user_byname(name)
    #print(user)
    if not user:
        return True
    else:
        return str(user[0]['id']) == str(uid)


# update功能预检查数据
def valid_update_user(params):
    #初始化函数内变量
    user = {}
    error = {}
    is_valid = True
    #检查用户是否有效
    user['id'] = params.get('uid').strip()
    if get_user(user['id']) is None:
        error['id'] = '用户数据无效'
        is_valid = False

    #检查用户名是否存在
    user['name'] = params.get('username').strip()
    if not vaild_name_unique(user['name'],user['id']):
        is_valid = False
        error['name'] = '用户名已存在'

    #检查年龄格式是否正确
    user['age'] = params.get('age').strip()
    if not user['age'].isdigit():
        error['age'] = '年龄格式错误'
        is_valid = False

    user['tel'] = params.get('tel').strip()
    user['sex'] = int(params.get('sex'))
    #print(user)
    return user,is_valid,error


#把用户信息update到数据文件中
def update_user(user):
    #print(user)
    cnt,result = mysql_connection.mysql_ut(SQL_UPDATE_USER,(user['name'],user['age'],user['tel'],user['sex'],user['id']),fetch=False)
    return True


#验证创建用户信息
def valid_create_user(params):

    is_valid = True
    user = {}
    error = {}

    user['name'] = params.get('username','').strip()
    if user['name'] == '':
        is_valid = False
        error['name'] = '名字不能为空'
    else:
        if get_user_byname(user['name']):
                is_valid = False
                error['name'] = '用户名已存在'

    user['age'] = params.get('age','0').strip()
    if not user['age'].isdigit():
        is_valid = False
        error['age'] = '年龄格式错误'

    user['sex'] = params.get('sex','0')
    user['tel'] = params.get('tel','')
    user['password'] = params.get('password1').strip()
    if user['password'] == '' or user['password'] != params.get('password2').strip():
        is_valid = False
        error['password'] = '密码不能为空或两次输入不同'

    return is_valid,user,error


def create_user(user):
    #print(user)
    cnt,result = mysql_connection.mysql_ut(SQL_CREATE_USER,(user['name'],user['age'],user['tel'],user['sex'],user['password']),fetch=False)
    return True


def get_user_password(uid):
    cnt,user = mysql_connection.mysql_ut(SQL_USER_PASSWORD,(str(uid),))
    return user


def valid_cp(params,param):
    errors = {}
    is_valid = True

    if params.get('old_password').strip() == '':
        is_valid = False
        errors['old_password'] = '密码不能为空'

    if params.get('old_password').strip() != get_user_password(param.get('user')['id'])[0].get('password'):
        is_valid = False
        errors['old_password'] = '你输入的密码不正确'

    if params.get('new1_password').strip() != params.get('new2_password').strip() or params.get('new1_password').strip() == '':
        is_valid = False
        errors['new_password'] = '密码不能为空或两次输入不同'

    return is_valid,params.get('new1_password').strip(),param.get('user')['id'],errors


def cp(uid,new_password):
    cnt,result = mysql_connection.mysql_ut(SQL_CHANGE_PASSWORD,(new_password,uid),fetch=False)
    return True
