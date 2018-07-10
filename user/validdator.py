# encoding: utf-8

from django.utils import timezone
from .models import User

class Validator(object):

    @classmethod
    def is_integer(cls,value):
        try:
            int(value)
            return True
        except BaseException as e:
            print(e)
            return False


class UserValidator(Validator):

    @classmethod
    def valid_login(cls,name,password):
        user = None
        try:
            user = User.objects.get(name=name)
        except BaseException as e:
            pass

        if user is None:
            return None

        if password == user.password:
            return user

        return None


    @classmethod
    def vaild_name_unique(cls,name,uid=None):
        user = None
        try:
            user = User.objects.get(name=name)
        except Exception as e:
            pass

        #print(user)
        if user is None:
            return True
        else:
            return str(user.id) == str(uid)


    @classmethod
    def valid_update_user(cls,params):
        #初始化函数内变量
        user = None
        error = {}
        is_valid = True

        #检查用户是否有效
        try:
            user = User.objects.get(pk=params.get('uid').strip())
        except BaseException as e:
            error['name'] = '用户数据无效'
            is_valid = False
            return user,is_valid,error

        #检查用户名是否存在
        name = params.get('username').strip()
        if name == '':
            error['name'] = '用户名不能为空'
            is_valid = False
        elif not cls.vaild_name_unique(name, user.id):
            is_valid = False
            error['name'] = '用户名已存在'
        else:
            user.name = name

        #检查年龄格式是否正确
        age = params.get('age').strip()
        if not cls.is_integer(age):
            error['age'] = '年龄格式错误'
            is_valid = False
        else:
            user.age = int(age)

        user.tel = params.get('tel').strip()
        user.sex = int(params.get('sex'))
        user.addr = params.get('addr').strip()
        return user,is_valid,error

    @classmethod
    def valid_create_user(cls,params):

        is_valid = True
        user = User()
        error = {}

        user.name = params.get('username','').strip()
        #检查用户名
        if user.name  == '':
            error['name'] = '用户名不能为空'
            is_valid = False

        if not cls.vaild_name_unique(user.name):
            is_valid = False
            error['name'] = '用户名重复'
            print('check username')
        else:
            pass

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
        user.create_time = timezone.now()
        return is_valid,user,error


    @classmethod
    def valid_cp(cls,params,uid):
        errors = {}
        is_valid = True

        user = User.objects.get(pk=uid)
        print(uid)
        print(params)
        if params.get('old_password').strip() == '':
            is_valid = False
            errors['old_password'] = '密码不能为空'
        elif params.get('old_password').strip() != user.password:
            is_valid = False
            errors['old_password'] = '你输入的密码不正确'
        elif params.get('new1_password').strip() != params.get('new2_password').strip() or params.get('new1_password').strip() == '':
            is_valid = False
            errors['new_password'] = '密码不能为空或两次输入不同'
        else:
            user.password = params.get('new1_password').strip()

        return is_valid,user,errors