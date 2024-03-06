from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('/', views.index, name='index'),
    path('/dashboard', views.dashboard, name='dashboard'),
    path('/login', views.login_view, name='login'),
    path('/auth', views.auth, name='auth'),
    path('/logout', views.logout, name='logout'),
    path('/restaurant_menus', views.restaurant_menus, name='restaurant_menus'),
    path('/add_menu_item', views.add_menu_item, name='add_menu_item'),
    path('/add_menu', views.add_menu, name='add_menu'),
    path('/insert_menu', views.insert_menu, name='insert_menu'),
    path('/view_menu/<int:restaurant_menu>', views.view_menu, name='view_menu'),
    path('/edit_menu/<int:restaurant_menu>', views.edit_menu, name='edit_menu'),
    path('/update_menu/<int:restaurant_menu>', views.update_menu, name='update_menu')
]