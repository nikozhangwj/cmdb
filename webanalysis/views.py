# encoding: utf-8
import os, time, json
from functools import wraps
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import AccessLogFile, AccessLog
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
    files = AccessLogFile.objects.filter(status=0).order_by('-created_time')[:10]
    return render(request, 'webanalysis/index.html',{"files" : files})

@login_required
def upload(request):
    log = request.FILES.get('log', None)
    if log:
        path = os.path.join(settings.BASE_DIR, 'media', 'uploads', str(time.time()))
        fhandler = open(path, 'wb')

        for chunk in log.chunks():
            fhandler.write(chunk)
        fhandler.close()

        obj = AccessLogFile(name=log.name, path=path)
        obj.save()

        path = os.path.join(settings.BASE_DIR, 'media', 'notices', str(time.time()))
        with open(path,'w') as fhandler:
            fhandler.write(json.dumps({'id' : obj.id, 'path' : obj.path}))

    return HttpResponse('upload')

@login_required
def dist_status_code(request):
    legend, series = AccessLog.dist_status_code(request.GET.get('id',0))
    print(legend, series)
    return JsonResponse({'code' : 200, 'result' : {"legend" : legend, 'series' : series}})

@login_required
def trend_visit(request):
    xAxis, series = AccessLog.trend_visit(request.GET.get('id',0))
    print(xAxis, series)
    return JsonResponse({'code' : 200, 'result' : {"xAxis" : xAxis, 'series' : series}})