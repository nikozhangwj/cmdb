# encoding: utf-8

from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

from .models import get_user, valid_login
curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    #return HttpResponse(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    return render(request, 'user/index.html', {'curr_time':curr_time,'users':get_user()})


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
    print(uid)