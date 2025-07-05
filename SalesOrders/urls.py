from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path("orders/", views.SalesOrder, name='SalesOrder')
    
    path("orders/", views.sales_order_list, name="orders"),
    path("logout/", LogoutView.as_view(), name="logout")
]