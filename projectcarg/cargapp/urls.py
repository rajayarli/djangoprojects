from django.contrib import admin
from django.urls import path
from cargapp import views
urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('register',views.register,name='register'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('logout',views.logout,name='logout'),
    path('bulkregister',views.bulkregister,name='bulkregister'),
]