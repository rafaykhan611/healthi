from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from admin.models import *
from restaurants.models import *
from home.models import *
from restaurants.models import *
from django.forms.models import model_to_dict
from Healthi.decorators import *


def login_view(request):
    if "admin_login" in request.session:
        return redirect(reverse('admin:dashboard'))
    err = request.GET.get('err')
    return render(request, 'admin/login.html', {"err":err})


def auth(request):
    if "admin_login" in request.session:
        return redirect(reverse('admin:dashboard'))
    if request.method == "POST":
        data = request.POST
        user = admins.objects.filter(username=data.get('username'), password=data.get('password')).first()
        if not user == None:
            request.session['admin_login'] = user.first_name
            return redirect(reverse('admin:dashboard'))
        else:
            return redirect(reverse('admin:login')+"?err=true")
    else:
        return redirect(reverse('admin:login')+"?err=true")

def logout(request):
    if "admin_login" in request.session:
        del request.session['admin_login']
    return redirect(reverse('admin:login'))

@isLoggedIn
def dashboard(request):
    data = {'restaurants':restaurants.objects.all().__len__(), 'clients':users.objects.all().__len__()}
    return render(request, 'admin/dashboard.html',data)

@isLoggedIn
def rrestaurants(request):
    page_name = 'Restaurants'
    data = [model_to_dict(restaurant) for restaurant in restaurants.objects.all()]
    return render(request, 'admin/restaurants.html', {'page_name':page_name, 'restaurants':data})


@isLoggedIn
def restaurant(request, pk):
    data = model_to_dict(restaurants.objects.get(id=pk))
    orderss = order_items.objects.filter(item__restaurant__id=pk)
    page_name = 'View '+data.get('name')
    return render(request, 'admin/restaurant_view.html', {'page_name':page_name, 'restaurant':data, 'orderss':orderss})

@isLoggedIn
def restaurant_add(request):
    page_name = 'Add New Restaurant'
    return render(request, 'admin/restaurant_add.html', {'page_name':page_name})

@isLoggedIn
def restaurant_insert(request):
    if request.method == 'POST':
        data = request.POST
        img =  request.FILES.get('image',False)
        img = handle_uploaded_file(img,"restaurants/img/restaurants")
        restaurant = restaurants.objects.create(name=data.get("name"), status=data.get("status"), image=img, description=data.get("description"), username=data.get("username"), password=data.get("password"))
        if restaurant:
            messages.success(request, "Added New Restaurant")
        else:
            messages.error(request, "Something went wrong in adding New Restaurant")
    return redirect(reverse("admin:restaurants"))

@isLoggedIn
def restaurant_edit(request,pk):
    data = model_to_dict(restaurants.objects.get(id=pk))
    page_name = 'Edit '+data.get('name')
    return render(request, 'admin/restaurant_edit.html', {'page_name':page_name, 'restaurant':data})

@isLoggedIn
def restaurant_update(request,pk):
    if request.method == 'POST':
        data = request.POST
        img =  request.FILES.get('image',False)
        img = handle_uploaded_file(img,"restaurants/img/restaurants")
        restaurant = restaurants.objects.filter(id=pk).update(name=data.get("name"), status=data.get("status"), image=img, description=data.get("description"), username=data.get("username"), password=data.get("password"))
        if restaurant:
            messages.success(request, "Updated Restaurant")
        else:
            messages.error(request, "Something went wrong in Updating Restaurant")
    return redirect(reverse("admin:restaurants"))

@isLoggedIn
def add_menu_item(request, restaurant):
    if request.method == 'POST':
        data = request.POST
        img =  request.FILES.get('image',False)
        img = handle_uploaded_file(img,"restaurants/img/menu_items")
        menu_item = menu_items.objects.create(name=data.get("name"),calories=data.get("calories"),description=data.get("description"),image=img, restaurant_id = restaurant)
        if menu_item:
            messages.success(request, "New Menu Item Added")
        else:
            messages.error(request, "Something went wrong in Adding New Menu Item")
    return redirect(reverse("admin:restaurant_menus",kwargs={'pk':restaurant}))

@isLoggedIn
def restaurant_menus(request, pk):
    data = model_to_dict(restaurants.objects.get(id=pk))
    page_name = data.get('name')+' Menu'
    restaurant_menus = (menu.objects.filter(restaurant__id=pk))
    return render(request, 'admin/restaurant_menus.html', {'page_name':page_name, 'restaurant':data, 'restaurant_menus':restaurant_menus})

@isLoggedIn
def add_menu(request, restaurant):
    data = model_to_dict(restaurants.objects.get(id=restaurant))
    page_name = 'Add Menu'
    items = menu_items.objects.filter(restaurant__id=restaurant)
    return render(request, 'admin/restaurant_add_menu.html', {'page_name':page_name, 'restaurant':data, 'menu_items':items})

@isLoggedIn
def insert_menu(request, restaurant):
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
    return redirect(reverse("admin:restaurant_menus",kwargs={'pk':restaurant}))


@isLoggedIn
def view_menu(request,restaurant_menu):
    data = model_to_dict(menu.objects.get(id=restaurant_menu))
    page_name = 'View '+data.get('name')
    bundles = {
        'breakfast': bundle.objects.filter(menu_id=restaurant_menu, type_id=1),
        'lunch': bundle.objects.filter(menu_id=restaurant_menu, type_id=2),
        'dinner': bundle.objects.filter(menu_id=restaurant_menu, type_id=3),
    }
    
    return render(request, 'admin/restaurant_view_menu.html', {'page_name':page_name, 'menu':data, 'bundle':bundles})


@isLoggedIn
def edit_menu(request,restaurant_menu):
    data = model_to_dict(menu.objects.get(id=restaurant_menu))
    page_name = 'Edit '+data.get('name')
    items = menu_items.objects.filter(restaurant=data.get('restaurant'))
    bundles = {
        'breakfast': list(item.menu_item.id for item in (bundle.objects.filter(menu_id=restaurant_menu, type_id=1))),
        'lunch': list(item.menu_item.id for item in (bundle.objects.filter(menu_id=restaurant_menu, type_id=2))),
        'dinner': list(item.menu_item.id for item in (bundle.objects.filter(menu_id=restaurant_menu, type_id=3))),
    }
    
    return render(request, 'admin/restaurant_edit_menu.html', {'page_name':page_name, 'menu':data, 'bundle':bundles, 'menu_items':items})

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
    return redirect(reverse("admin:restaurant_menus",kwargs={'pk':menu.objects.get(id=restaurant_menu).restaurant_id}))
    


@isLoggedIn
def customers(request):
    data = users.objects.all()
    return render(request, 'admin/customers.html', {'customers':data})

@isLoggedIn
def customer_view(request,pk):
    data = users.objects.get(id=pk)
    cd = details.objects.filter(user=data).first()
    return render(request, 'admin/customer_view.html', {'customer':data, 'customer_details':cd})

@isLoggedIn
def customer_orders(request):
    pk = request.GET.get('pk')
    user = users.objects.filter(id=pk).first()
    
    porders = orders.objects.filter(user=user)
    borders = []
    
    for o in porders:
        oitems = order_items.objects.filter(order_id=o.id)
        borders.append({'order':o,'items':oitems})
        
    return render(request, 'admin/customers_orders.html', {'orderss':borders})

@isLoggedIn
def vorders(request):
    data = model_to_dict(restaurants.objects.all())
    return render(request, 'admin/restaurants.html', {'restaurants':data})
