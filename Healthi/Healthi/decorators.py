from django.http import HttpResponseRedirect
from Healthi.settings import MEDIA_ROOT
import os
import time

def isLoggedIn(function):
    def wrapper(request, *args, **kwargs):
        app_name = request.resolver_match.app_name
        print(app_name)
        if app_name+"_login" not in request.session.keys():
            return HttpResponseRedirect("/"+app_name+"/login")
        else:
            return function(request, *args, **kwargs)
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

def handle_uploaded_file(f,dir):
    if f == False:
        return dir+'/default.png'
    if not os.path.exists(os.path.join(MEDIA_ROOT, dir)):
        os.makedirs(os.path.join(MEDIA_ROOT, dir))
    name = dir+'/'+str(round(time.time() * 1000)) + "." + f.name.split('.')[1]
    with open(os.path.join(MEDIA_ROOT, name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name

def delete_file(f):
    f =  os.path.join(MEDIA_ROOT, f)
    os.remove(f)