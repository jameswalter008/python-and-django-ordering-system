from accounts.models import Customer
from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('customers/<str:id>',views.customers,name="customers.show"),#str could be int or slug too
    path('customer_profile',views.customer_profile,name="customers.customer_profile"),#str could be int or slug too
    path('products/',views.products,name="products"),
    path('order/create/<int:customerid>',views.ordercreate,name="orders.create"),
    path('order/update/<int:orderid>',views.orderupdate,name="order.update"),
    path('order/delete/<int:orderid>',views.orderDelete,name="order.delete"),
    path('register/',views.register,name="register"),
    path('login/',views.userlogin,name="login"),
    path('logout/',views.userlogout,name="logout")
]