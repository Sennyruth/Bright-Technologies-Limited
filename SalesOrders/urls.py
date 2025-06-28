from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path("orders/", views.SalesOrder, name='SalesOrder')
    
    path("orders/", views.sales_order_list, name="orders"),

]