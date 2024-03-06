from django.shortcuts import render,redirect
from django.urls import reverse
from restaurants.models import *
from home.models import *
from Healthi.decorators import *
from django.forms.models import model_to_dict

def login_view(request):
    if "restaurants_login" in request.session:
        return redirect(reverse('restaurants:dashboard'))
    err = request.GET.get('err')
    return render(request, 'restaurants/login.html', {"err":err})


def auth(request):
    if "restaurants_login" in request.session:
        return redirect(reverse('restaurants:dashboard'))
    if request.method == "POST":
        data = request.POST
        user = restaurants.objects.filter(username=data.get('username'), password=data.get('password')).first()
        if not user == None:
            request.session['restaurants_login'] = user.name
            request.session['restaurnts_id'] = user.id
            return redirect(reverse('restaurants:dashboard'))
        else:
            return redirect(reverse('restaurants:login')+"?err=true")
    else:
        return redirect(reverse('restaurants:login')+"?err=true")

def logout(request):
    if "restaurants_login" in request.session:
        del request.session['restaurants_login']
        del request.session['restaurnts_id']
    return redirect(reverse('restaurants:login'))

@isLoggedIn
def index(request):
    pass

@isLoggedIn
def dashboard(request):
    data = model_to_dict(restaurants.objects.get(id=request.session['restaurnts_id']))
    orderss = order_items.objects.filter(item__restaurant__id=request.session['restaurnts_id'])
    page_name = 'View '+data.get('name')
    return render(request, 'restaurants/dashboard.html', {'page_name':page_name, 'restaurant':data, 'orderss':orderss})

