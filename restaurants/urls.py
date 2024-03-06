from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('/', views.index, name='index'),
    path('/dashboard', views.dashboard, name='dashboard'),
    path('/login', views.login_view, name='login'),
    path('/auth', views.auth, name='auth'),
    path('/logout', views.logout, name='logout'),
]