from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='home'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('auth', views.auth, name='auth'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('save_details', views.save_details, name='save_details'),
    path('profile', views.profile, name='profile'),
    path('home', views.index, name='hhome'),
    path('about', views.about, name='about'),
    path('contact_us', views.contact, name='contact_us'),
    path('all_restaurants', views.rrestaurants, name='restaurants'),
    path('view_restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_view'),
    path('add_to_cart/<int:pk>/<int:type>', views.add_to_cart, name='add_to_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('remove_cart_item/<int:menu>', views.remove_cart_item, name='remove_cart_item'),
    path('past_orders', views.past_orders, name='past_orders'),
]