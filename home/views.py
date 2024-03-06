from django.shortcuts import render, redirect
from django.urls import reverse
from restaurants.models import *
from home.models import *
from Healthi.decorators import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.forms.models import model_to_dict
# Create your views here.


def index(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    return render(request, 'home/index.html',{'cart':cart,'pp':pp})

def about(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    return render(request, 'home/about.html',{'cart':cart,'pp':pp})

def contact(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    return render(request, 'home/contact.html',{'cart':cart,'pp':pp})

def rrestaurants(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    res = restaurants.objects.filter(status='Y')
    return render(request, 'home/restaurants.html',{'restaurants':res,'cart':cart,'pp':pp})


def restaurant_detail(request, pk):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    restaurant = restaurants.objects.get(id=pk)
    mmenus = menu.objects.filter(restaurant=pk)
    lmenus = []
    for m in mmenus:
        lmenus.append({'menu':m, 'bundles' : {'breakfast': bundle.objects.filter(menu_id=m.id, type_id=1),'lunch': bundle.objects.filter(menu_id=m.id, type_id=2),'dinner': bundle.objects.filter(menu_id=m.id, type_id=3)}})
    
    return render(request, 'home/restaurant_view.html',{'restaurant':restaurant, 'menus':lmenus,'cart':cart,'pp':pp})

def sign_in(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    if "home_login" in request.session:
        return redirect(reverse('home:home'))
    return render(request, 'home/sign_in.html',{'cart':cart,'pp':pp})


def sign_up(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    if "home_login" in request.session:
        return redirect(reverse('home:home'))
    return render(request, 'home/sign_up.html',{'cart':cart,'pp':pp})

def logout(request):
    if "home_login" in request.session:
        del request.session['home_login']
        del request.session['calories']
    return redirect(reverse('home:sign_in'))

def auth(request):
    if "home_login" in request.session:
        return redirect(reverse('home:profile'))
    if request.method == "POST":
        data = request.POST
        user = users.objects.filter(email=data.get('email'), password=data.get('password')).first()
        if not user == None:
            request.session['home_login'] = user.email
            detail = details.objects.filter(user=user)
            if detail.first():
                request.session['calories'] = detail.first().calories
                return redirect(reverse('home:home'))
            else:
                return redirect(reverse('home:profile'))
        else:
            return redirect(reverse('home:sign_in')+"?err=true")
    else:
        return redirect(reverse('home:sign_in')+"?err=true")

def register(request):
    if request.method == 'POST':
        data = request.POST
        user = users.objects.create(first_name=data.get('first_name'),last_name=data.get('last_name'),contact=data.get('contact'),address=data.get('address'),email=data.get('email'),password=data.get('password'),age=data.get('age'),gender=data.get('gender'))
        if user:
            request.session['home_login'] = user.email
            return redirect(reverse('home:profile'))

@csrf_exempt
def save_details(request):
    if request.method == 'POST':
        data = request.POST
        users.objects.filter(email=request.session['home_login'])
        user = users.objects.get(email=request.session['home_login'])
        detail = details.objects.filter(user=user)
        if detail:
            detail.delete()
        detail = details.objects.create(bmi=data.get('bmi'),calories=data.get('cal'), user=user, weight=data.get('weight'),height_in=data.get('height_in'),height_feet=data.get('height_feet'),activity_level=data.get('activity'),weight_goal=data.get('goal'),)
        request.session['calories'] = detail.calories
        if detail:
            return redirect(reverse('home:profile'))

def profile(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    user = users.objects.filter(email=request.session['home_login']).first()
    user_details = details.objects.filter(user__email=request.session['home_login']).first()
    if user_details:
        request.session['calories'] = user_details.calories
    return render(request, 'home/user_profile.html',{'user_details':user_details, 'user':user,'cart':cart,'pp':pp})

def add_to_cart(request,pk,type):
    # if not request.session['cart']:
    if 'cart' in request.session:
        newcart = request.session['cart']
        newcart.append({'menu':pk, 'plan':type})
        request.session['cart'] = newcart
    else:
        request.session['cart'] = [{'menu':pk, 'plan':type}]
    print(request.session['cart'],'hahaha')
    referring_url = request.META.get('HTTP_REFERER')

    # If the referring URL is available, redirect to it; otherwise, redirect to a default URL
    return redirect(referring_url) if referring_url else redirect('fallback_url')

def remove_cart_item(request,menu):
    
    filtered_data = [item for item in request.session['cart'] if item.get('menu') != menu]
    request.session['cart'] = filtered_data
    referring_url = request.META.get('HTTP_REFERER')

    # If the referring URL is available, redirect to it; otherwise, redirect to a default URL
    return redirect(referring_url) if referring_url else redirect('fallback_url')

def checkout(request):
    if not 'home_login' in request.session:
        return redirect(reverse('home:sign_in'))
    else:
        user = users.objects.filter(email=request.session['home_login']).first()
        pp = 0
        if 'cart' in request.session:
            for c in request.session['cart']:
                m = menu.objects.get(id=c.get('menu'))
                price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
                pp += price
            
        o = orders.objects.create(user=user, total_amount=pp)
        recipient_list = []
        if 'cart' in request.session:
            for c in request.session['cart']:
                m = menu.objects.get(id=c.get('menu'))
                price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
                plan = 'd' if c.get('plan') == 1 else 'w' if c.get('plan') == 2 else 'y' if c.get('plan') == 3 else None
                recipient_list.append(m.restaurant.email)
                order_items.objects.create(order=o,item=m,plan=plan,price=price)
        
        request.session['cart']=[]
        # orders.objects.create()
        subject = 'New Order'
        message = f'A new order has been placed by {user.first_name} sign in to your account to complete the order'
        from_email = 'healthimeal@outlook.com'

        send_mail(subject, message, from_email, recipient_list)
        
        return redirect(reverse('home:home'))

def past_orders(request):
    cart = []
    pp = 0
    if 'cart' in request.session:
        for c in request.session['cart']:
            m = menu.objects.get(id=c.get('menu'))
            price = m.daily_plan_price if c.get('plan') == 1 else m.weekly_plan_price if c.get('plan') == 2 else m.yearly_plan_price if c.get('plan') == 3 else None
            cart.append({'menu':m,'plan':price})
            pp += price
    user = users.objects.filter(email=request.session['home_login']).first()
    
    porders = orders.objects.filter(user=user)
    borders = []
    
    for o in porders:
        oitems = order_items.objects.filter(order_id=o.id)
        borders.append({'order':o,'items':oitems})
        
    
    return render(request, 'home/user_orders.html',{'orders':porders, 'borders':borders, 'user':user,'cart':cart,'pp':pp})