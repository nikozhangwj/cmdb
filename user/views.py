# encoding: utf-8

from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

from .models import get_users, get_user, valid_login, delete_user, valid_update_user, update_user
curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    #return HttpResponse(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    return render(request, 'user/index.html', {'curr_time':curr_time,'users':get_users()})


def login(request):
    if 'GET' == request.method:
        return render(request,'user/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        #username = 'niko'
        #password = '123'
        user = valid_login(username,password)
        if user:
            request.session['user']=user
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
            delete_user(uid)
        return redirect('user:index')
    else:
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':get_users()})

def user_info(request):
    if not request.session.get('user'):
        return redirect('user:login')

    uid = request.GET.get('uid','')
    if request.session.get('user')['id'] == uid:
        return render(request,'user/user_info.html',{'user':get_user(uid)})
    else:
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':get_users()})



def update(request):
    if not request.session.get('user'):
        return redirect('user:login')
    user,is_valid,error = valid_update_user(request.POST)
    if is_valid:
        update_user(user)
        return redirect('user:index')
    else:
        return render(request,'user/user_info.html',{'user' : user, 'errors' : error})