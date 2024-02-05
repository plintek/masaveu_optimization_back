from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersListApiView.as_view(), name='index'),
    path('<int:user_id>', views.UsersListApiView.as_view(), name='index'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('checkLogin', views.CheckLogin.as_view(), name='checkLogin'),
    path('logout', views.LogOut.as_view(), name='logout'),
]
