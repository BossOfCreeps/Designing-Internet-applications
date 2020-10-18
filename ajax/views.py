from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from core.models import Product, Order, OrderedProduct
import json


def count(request):
    ordered_product = OrderedProduct.objects.get(id=request.POST.get("id"))
    ordered_product.count = int(request.POST.get("val"))
    if ordered_product.count < 1:
        for order in Order.objects.all():
            if ordered_product in order.products.all():
                order.products.remove(ordered_product)
                return HttpResponse(json.dumps({"id": ordered_product.id, "product_price": ordered_product.sum_price,
                                                "order_price": order.price}))
    ordered_product.save()

    for order in Order.objects.all():
        if ordered_product in order.products.all():
            return HttpResponse(json.dumps({"id": ordered_product.id, "product_price": ordered_product.sum_price,
                                            "order_price": order.price}))
