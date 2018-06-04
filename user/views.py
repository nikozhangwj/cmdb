# encoding: utf-8

from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
# Create your views here.
from .models import User
from .models import get_users, get_user, valid_login, delete_user, valid_update_user, update_user, valid_create_user, create_user, valid_cp, cp
curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    #return HttpResponse(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    return render(request, 'user/index.html', {'curr_time':curr_time,'users':User.get_list()})


def login(request):
    if request.session.get('user'):
        return redirect('user:index')
    if 'GET' == request.method:
        return render(request,'user/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.valid_login(username,password)
        if user:
            request.session['user']=user.as_dict()
            return redirect('user:index')
            #return render(request,'user/index.html',{'curr_time':curr_time,'users':get_user().items()})
        else:
            return render(request,'user/login.html',{'name': username, 'errors':{'default':'用户名或密码错误'}})


def user_logout(request):
    request.session.flush()
    return redirect('user:login')


def delete(request):
    if not request.session.get('user'):
        return redirect('user:login')
    uid = request.GET.get('uid')
    if request.session.get('user')['name'] == 'Admin':
        if uid.isdigit():
            User.delete_user(uid)
        return redirect('user:index')
    else:
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':User.get_list()})

def user_info(request):
    if not request.session.get('user'):
        return redirect('user:login')

    uid = request.GET.get('uid','')
    if request.session.get('user')['id'] == uid or request.session.get('user')['name'] == 'Admin':
        return render(request,'user/user_info.html',{'user':User.get_user_by_id(uid)})
    else:
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':User.get_list()})



def update(request):
    if not request.session.get('user'):
        return redirect('user:login')
    user,is_valid,error = User.valid_update_user(request.POST)
    if is_valid:
        user.update_user()
        return redirect('user:index')
    else:
        return render(request,'user/user_info.html',{'user' : user, 'errors' : error})


def create(request):
    if not request.session.get('user'):
        return redirect('user:login')
    if request.session.get('user')['name'] != 'Admin':
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':User.get_list()})
    if 'GET' == request.method:
        return render(request,'user/create.html')
    else:
        is_valid,user,error = valid_create_user(request.POST)
        if is_valid:
            create_user(user)
            return redirect('user:index')
        else:
            return render(request,'user/create.html',{'errors':error})


def change_password(request):
    if not request.session.get('user'):
        return redirect('user:login')
    if 'GET' == request.method:
        return render(request,'user/change_password.html')
    else:
        is_valid,new_password,uid,errors = valid_cp(request.POST,request.session)
        if is_valid:
            cp(uid,new_password)
            return redirect('user:index')
        else:
            return render(request,'user/change_password.html',{'errors':errors})
