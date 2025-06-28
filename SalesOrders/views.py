from django.shortcuts import render, HttpResponse
from .models import SalesOrder

# Create your views here.
def home(request):
    # return HttpResponse("Hello, world. You're at the home page.")
    return render(request, "home.html")

# def SalesOrder(request):
#     order = SalesOrder.objects.all()
#     return render(request, "SalesOrders.html", {"SalesOrder": order})

def sales_order_list(request):
    orders = SalesOrder.objects.all()
    return render(request, "orders_list.html", {"orders": orders})
