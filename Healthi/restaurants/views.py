from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
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
    orderss = order_items.objects.filter(item__restaurant__id=request.session['restaurnts_id']).order_by('-order__order_date')
    page_name = 'View '+data.get('name')
    ordersss = []
    for o in orderss:
        reviews = review.objects.filter(order=orders.objects.get(id=o.order_id)).first()
        ordersss.append({'oi':o,'reviews':reviews})
    
    return render(request, 'restaurants/dashboard.html', {'page_name':page_name, 'restaurant':data, 'orderss':ordersss})


@isLoggedIn
def add_menu_item(request):
    restaurant =request.session['restaurnts_id']
    if request.method == 'POST':
        data = request.POST
        img =  request.FILES.get('image',False)
        img = handle_uploaded_file(img,"restaurants/img/menu_items")
        menu_item = menu_items.objects.create(name=data.get("name"),calories=data.get("calories"),description=data.get("description"),image=img, restaurant_id = restaurant)
        if menu_item:
            messages.success(request, "New Menu Item Added")
        else:
            messages.error(request, "Something went wrong in Adding New Menu Item")
    return redirect(reverse("restaurants:restaurant_menus"))

@isLoggedIn
def restaurant_menus(request):
    pk =request.session['restaurnts_id']
    data = model_to_dict(restaurants.objects.get(id=pk))
    page_name = data.get('name')+' Menu'
    restaurant_menus = (menu.objects.filter(restaurant__id=pk))
    return render(request, 'restaurants/restaurant_menus.html', {'page_name':page_name, 'restaurant':data, 'restaurant_menus':restaurant_menus})

@isLoggedIn
def add_menu(request):
    restaurant =request.session['restaurnts_id']
    data = model_to_dict(restaurants.objects.get(id=restaurant))
    page_name = 'Add Menu'
    items = menu_items.objects.filter(restaurant__id=restaurant)
    return render(request, 'restaurants/restaurant_add_menu.html', {'page_name':page_name, 'restaurant':data, 'menu_items':items})

@isLoggedIn
def insert_menu(request):
    restaurant =request.session['restaurnts_id']
    if request.method == 'POST':
        data = request.POST
        img =  request.FILES.get('image',False)
        img = handle_uploaded_file(img,"restaurants/img/menu")
        nmenu = menu.objects.create(name=data.get('name'), status=data.get('status'), description=data.get('description'),daily_plan_price=data.get('dpp'), weekly_plan_price=data.get('wpp'), monthly_plan_price=data.get('mpp'), restaurant=restaurants.objects.get(id=restaurant), image=img)
        for b in data.get('breakfast'):
            bundle.objects.create(menu=nmenu, type_id=1, menu_item=menu_items.objects.get(id=b))
        for l in data.get('lunch'):
            bundle.objects.create(menu=nmenu, type_id=2, menu_item=menu_items.objects.get(id=l))
        for d in data.get('dinner'):
            bundle.objects.create(menu=nmenu, type_id=3, menu_item=menu_items.objects.get(id=d))
        if nmenu:
            messages.success(request, "New Menu Added")
        else:
            messages.error(request, "Something went wrong in Adding New Menu")
    return redirect(reverse("restaurants:restaurant_menus"))


@isLoggedIn
def view_menu(request,restaurant_menu):
    data = model_to_dict(menu.objects.get(id=restaurant_menu))
    page_name = 'View '+data.get('name')
    bundles = {
        'breakfast': bundle.objects.filter(menu_id=restaurant_menu, type_id=1),
        'lunch': bundle.objects.filter(menu_id=restaurant_menu, type_id=2),
        'dinner': bundle.objects.filter(menu_id=restaurant_menu, type_id=3),
    }
    
    return render(request, 'restaurants/restaurant_view_menu.html', {'page_name':page_name, 'menu':data, 'bundle':bundles})


@isLoggedIn
def edit_menu(request,restaurant_menu):
    restaurant =request.session['restaurnts_id']
    data = model_to_dict(menu.objects.get(id=restaurant_menu))
    page_name = 'Edit '+data.get('name')
    items = menu_items.objects.filter(restaurant=restaurant)
    bundles = {
        'breakfast': list(item.menu_item.id for item in (bundle.objects.filter(menu_id=restaurant_menu, type_id=1))),
        'lunch': list(item.menu_item.id for item in (bundle.objects.filter(menu_id=restaurant_menu, type_id=2))),
        'dinner': list(item.menu_item.id for item in (bundle.objects.filter(menu_id=restaurant_menu, type_id=3))),
    }
    
    return render(request, 'restaurants/restaurant_edit_menu.html', {'page_name':page_name, 'menu':data, 'bundle':bundles, 'menu_items':items})

@isLoggedIn
def update_menu(request,restaurant_menu):
    if request.method == 'POST':
        data = request.POST
        img =  request.FILES.get('image',False)
        img = handle_uploaded_file(img,"restaurants/img/menu")
        nmenu = menu.objects.filter(id=restaurant_menu).update(name=data.get('name'), status=data.get('status'), description=data.get('description'),daily_plan_price=data.get('dpp'), weekly_plan_price=data.get('wpp'), monthly_plan_price=data.get('mpp'))
        bundle.objects.filter(menu_id=restaurant_menu).delete()
        for b in data.get('breakfast'):
            bundle.objects.create(menu_id=restaurant_menu, type_id=1, menu_item=menu_items.objects.get(id=b))
        for l in data.get('lunch'):
            bundle.objects.create(menu_id=restaurant_menu, type_id=2, menu_item=menu_items.objects.get(id=l))
        for d in data.get('dinner'):
            bundle.objects.create(menu_id=restaurant_menu, type_id=3, menu_item=menu_items.objects.get(id=d))
        if nmenu:
            messages.success(request, "Menu Updated")
        else:
            messages.error(request, "Something went wrong in Updating Menu")
    return redirect(reverse("restaurants:restaurant_menus"))
    

