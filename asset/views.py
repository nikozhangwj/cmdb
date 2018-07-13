#encoding: utf-8

from datetime import timedelta,datetime

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

from .models import Host, Resource
# Create your views here.

def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    return render(request, 'asset/index.html')


def list_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})
    result= [host.as_dict() for host in Host.objects.all()]
    return JsonResponse({'code' : 200, 'result' : result})


def list_info_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})
    try:
        _id = request.GET.get('id',0)
        #print(_id)
        host=Host.objects.get(id=_id).as_dict()
        #print(host)
        return JsonResponse({'code' : 200, 'result' : host})
    except BaseException as e:
        return JsonResponse({'code' : 404, 'result' : []})

def resource_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})
    try:
        _id = request.GET.get('id',0)
        host=Host.objects.get(id=_id)
        start_time = datetime.now() - timedelta(hours=1)
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


def update_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})