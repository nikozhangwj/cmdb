# encoding: utf-8

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
# Create your views here.
from .models import User
from .validdator import UserValidator

curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    #return HttpResponse(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    return render(request, 'user/index.html', {'curr_time':curr_time,'users':User.objects.all()})


def login(request):
    if request.session.get('user'):
        return redirect('user:index')
    if 'GET' == request.method:
        return render(request,'user/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserValidator.valid_login(username,password)
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
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':User.objects.all()})

def user_info(request):
    if not request.session.get('user'):
        return redirect('user:login')

    uid = request.GET.get('uid','')
    if request.session.get('user')['id'] == uid or request.session.get('user')['name'] == 'Admin':
        return render(request,'user/user_info.html',{'user':User.objects.get(id=uid)})
    else:
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':User.objects.all()})



def update(request):
    if not request.session.get('user'):
        return redirect('user:login')
    user,is_valid,error = UserValidator.valid_update_user(request.POST)
    if is_valid:
        user.save()
        return redirect('user:index')
    else:
        return render(request,'user/user_info.html',{'user' : user, 'errors' : error})


def create(request):
    if not request.session.get('user'):
        return redirect('user:login')
    if request.session.get('user')['name'] != 'Admin':
        return render(request,'user/index.html',{'errors':'你没有此操作权限', 'curr_time':curr_time, 'users':User.objects.all()})
    if 'GET' == request.method:
        return render(request,'user/create.html')
    else:
        is_valid,user,error = UserValidator.valid_create_user(request.POST)
        if is_valid:
            user.save()
            return redirect('user:index')
        else:
            return render(request,'user/create.html',{'errors':error})


def create_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code':403, 'errors':{'permission':'未登录'}})
    if request.session.get('user')['name'] != 'Admin':
        return JsonResponse({'code':403, 'errors':{'permission':'你没有此操作权限'}})
    else:
        is_valid,user,error = UserValidator.valid_create_user(request.POST)
        if is_valid:
            user.save()
            return JsonResponse({'code':200})
        else:
            return JsonResponse({'code':400, 'errors':error})


def change_password(request):
    uid = request.session.get('user')['id']
    if not request.session.get('user'):
        return redirect('user:login')
    if 'GET' == request.method:
        return render(request,'user/change_password.html')
    else:
        is_valid,user,errors = UserValidator.valid_cp(request.POST,uid)
        if is_valid:
            user.save()
            return redirect('user:index')
        else:
            return render(request,'user/change_password.html',{'errors':errors})


def change_password_ajax(request):
    uid = request.session.get('user')['id']
    if not request.session.get('user'):
        return redirect('user:login')
    else:
        is_valid,user,errors = UserValidator.valid_cp(request.POST,uid)
        if is_valid:
            user.save()
            return JsonResponse({'code' : 200})
        else:
            return JsonResponse({'code' : 400, 'errors' : errors})


def delete_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code':403, 'errors':{'permission':'未登录'}})
    uid = request.GET.get('id')
    if request.session.get('user')['name'] == 'Admin':
        if uid.isdigit():
            User.delete_user(uid)
            return JsonResponse({'code':200})
    else:
        return JsonResponse({'code':403, 'errors':{'permission':'你没有此操作权限'}})