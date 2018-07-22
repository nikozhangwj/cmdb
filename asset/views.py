#encoding: utf-8

from datetime import timedelta,datetime
from functools import wraps
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

from .models import Host, Resource
# Create your views here.

def login_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user') is None:
            if request.is_ajax():
                return JsonResponse({'code' : 403, 'result' : []})
            return redirect('user:login')

        return func(request, *args, **kwargs)
    return wrapper

@login_required
def index(request):
    return render(request, 'asset/index.html')

@login_required
def list_ajax(request):
    result= [host.as_dict() for host in Host.objects.all()]
    return JsonResponse({'code' : 200, 'result' : result})

@login_required
def list_info_ajax(request):
    try:
        _id = request.GET.get('id',0)
        #print(_id)
        host=Host.objects.get(id=_id).as_dict()
        #print(host)
        return JsonResponse({'code' : 200, 'result' : host})
    except BaseException as e:
        return JsonResponse({'code' : 404, 'result' : []})

@login_required
def resource_ajax(request):
    try:
        _id = request.GET.get('id',0)
        host=Host.objects.get(id=_id)
        start_time = datetime.now() - timedelta(hours=6)
        resources = Resource.objects.filter(ip=host.ip,created_time__gte=start_time).order_by('created_time')

        xAxis = []
        cpu_datas = []
        mem_datas = []

        for resource in resources:
            xAxis.append(resource.created_time.strftime('%Y-%m-%d %H:%M'))
            cpu_datas.append(resource.cpu)
            mem_datas.append(resource.mem)
        return JsonResponse({'code' : 200, 'result' : {'xAxis' : xAxis, 'cpu_datas' : cpu_datas, 'mem_datas' : mem_datas}})
    except BaseException as e:
        return JsonResponse({'code' : 403, 'result' : []})

@login_required
def update_ajax(request):
    pass