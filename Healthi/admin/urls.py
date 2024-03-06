from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('/', views.dashboard, name='index'),
    path('/dashboard', views.dashboard, name='dashboard'),
    path('/login', views.login_view, name='login'),
    path('/auth', views.auth, name='auth'),
    path('/logout', views.logout, name='logout'),
    path('/restaurants', views.rrestaurants, name='restaurants'),
    path('/restaurant_view/<int:pk>', views.restaurant, name='restaurant_view'),
    path('/restaurant_add', views.restaurant_add, name='restaurant_add'),
    path('/restaurant_insert', views.restaurant_insert, name='restaurant_insert'),
    path('/restaurant_edit/<int:pk>', views.restaurant_edit, name='restaurant_edit'),
    path('/restaurant_update/<int:pk>', views.restaurant_update, name='restaurant_update'),
    path('/restaurant_menus/<int:pk>', views.restaurant_menus, name='restaurant_menus'),
    path('/add_menu_item/<int:restaurant>', views.add_menu_item, name='add_menu_item'),
    path('/add_menu/<int:restaurant>', views.add_menu, name='add_menu'),
    path('/insert_menu/<int:restaurant>', views.insert_menu, name='insert_menu'),
    path('/view_menu/<int:restaurant_menu>', views.view_menu, name='view_menu'),
    path('/edit_menu/<int:restaurant_menu>', views.edit_menu, name='edit_menu'),
    path('/update_menu/<int:restaurant_menu>', views.update_menu, name='update_menu'),
    path('/customers', views.customers, name='customers'),
    path('/customer_view/<int:pk>', views.customer_view, name='customer_view'),
    path('/customer_orders', views.customer_orders, name='customer_orders'),
    path('/orders', views.vorders, name='orders'),

]