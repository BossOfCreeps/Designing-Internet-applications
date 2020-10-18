from datetime import datetime
from random import random

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.shortcuts import render, HttpResponseRedirect

from core.models import Product, Category, Manufacturer, Material, Image, Feedback, Advertising, Order, BaseProduct, \
    Address, PaymentMethod, OrderedProduct, Status, BaseStatus


def index(request):
    products = [Product.objects.order_by("-id").filter(base_product=bp)[0] for bp in BaseProduct.objects.all()]
    return render(request, "index.html", {"products": sorted(products, key=lambda x: random()),
                                          "categories": Category.objects.all(),
                                          "advertisements": Advertising.objects.all()})


def authenticating(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST.get("login"))
        if user.check_password(request.POST.get("password")):
            login(request, user)

    return HttpResponseRedirect(request.GET.get("path"))


def deauthenticating(request):
    if request.method == "GET":
        logout(request)

    return HttpResponseRedirect("/")


def product(request, product_id):
    base_pro = BaseProduct.objects.get(id=product_id)
    try:
        products = [
            ord_prod.product.base_product
            for order_ in Order.objects.filter(user=request.user, status__base_status_id=3)
            for ord_prod in order_.products.all()
        ]
    except:
        products = []
    product_ = Product.objects.order_by("-id").filter(base_product=base_pro)[0]
    return render(request, "product.html", {"product": product_, "can_feed": product_.base_product in products,
                                            "feedbacks": Feedback.objects.filter(product__id=product_id),
                                            "categories": Category.objects.all(),
                                            "advertisements": Advertising.objects.all()})


def reg_form(request):
    if request.method == "POST":
        u = User.objects.create_user(request.POST.get("login"), request.POST.get("email"), request.POST.get("password"))
        login(request, u)

    return HttpResponseRedirect("/")


def add_feedback(request, product_id):
    if request.method == 'POST':
        feedback = Feedback(user=request.user, text=request.POST.get("text"), rate=int(request.POST.get("rate")),
                            datetime=datetime.now(), product=BaseProduct.objects.get(id=product_id))
        feedback.save()
        if request.FILES:
            for photo in request.FILES.getlist("photos"):
                image = Image(image=photo)
                image.save()
                feedback.images.add(image)
            feedback.save()

    return HttpResponseRedirect(f"/product/{product_id}")


def catalog(request, category_id):
    base_products = BaseProduct.objects.filter(category_id=category_id)
    products = Product.objects.filter(base_product__category_id=category_id)
    widths = [product_.width for product_ in base_products]
    heights = [product_.height for product_ in base_products]
    prices = [Product.objects.order_by("-id").filter(base_product=bp)[0].price for bp in base_products]

    width_max = request.GET.get("width_max", max(widths))
    width_min = request.GET.get("width_min", min(widths))
    height_max = request.GET.get("height_max", max(heights))
    height_min = request.GET.get("height_min", min(heights))
    price_max = request.GET.get("price_max", max(prices))
    price_min = request.GET.get("price_min", min(prices))

    products = products.filter(price__gte=price_min, price__lte=price_max,
                               base_product__width__gte=width_min, base_product__width__lte=width_max,
                               base_product__height__gte=height_min, base_product__height__lte=height_max)

    sel_manufacturer_id = request.GET.get("manufacturer", None)
    if not str(sel_manufacturer_id).isnumeric():
        sel_manufacturer_id = None
    if sel_manufacturer_id is not None:
        products = products.filter(base_product__manufacturer__id=sel_manufacturer_id)

    sel_material_id = request.GET.get("material", None)
    if not str(sel_material_id).isnumeric():
        sel_material_id = None
    if sel_material_id is not None:
        products = products.filter(base_product__material__id=sel_material_id)

    clean_products = {}
    for product_ in products:
        clean_products[product_.base_product.id] = product_

    return render(request, "catalog.html", {
        "products": clean_products.values(), "category_id": category_id, "advertisements": Advertising.objects.all(),
        "manufacturers": Manufacturer.objects.all(), "materials": Material.objects.all(),
        "sel_manufacturer": None if sel_manufacturer_id is None else Manufacturer.objects.get(id=sel_manufacturer_id),
        "sel_material": None if sel_material_id is None else Material.objects.get(id=sel_material_id),
        "width_max": width_max, "width_min": width_min, "widths_max": max(widths), "widths_min": min(widths),
        "height_max": height_max, "height_min": height_min, "heights_max": max(heights), "heights_min": min(heights),
        "price_max": price_max, "price_min": price_min, "prices_max": max(prices), "prices_min": min(prices),
    })


def search(request):
    query = request.GET.get("q", "").lower()
    products = []
    categories = []
    for product_ in Product.objects.all():
        if product_.base_product.description.lower().find(query) != -1:
            products.append(product_)
            categories.append(product_.base_product.category)

    clean_products = {}
    for product_ in products:
        clean_products[product_.base_product.id] = product_
    return render(request, "search.html", {"products": clean_products.values(),
                                           "categories": set(categories), "advertisements": Advertising.objects.all()})


def profile(request):
    return render(request, "profile.html", {"orders": Order.objects.filter(user=request.user),
                                            "categories": Category.objects.all(),
                                            "advertisements": Advertising.objects.all()})


def profile_edit_form(request):
    if request.method == "POST":
        if request.POST.get("email"):
            request.user.email = request.POST.get("email")
            request.user.save()
        if request.POST.get("password"):
            request.user.set_password(request.POST.get("password"))
            request.user.save()
            login(request, request.user)
    return HttpResponseRedirect("/profile")


def order(request, order_id):
    return render(request, "order.html", {"order": Order.objects.get(id=order_id),
                                          "categories": Category.objects.all(),
                                          "advertisements": Advertising.objects.all()})


def basket(request):
    if Order.objects.filter(user=request.user, status__base_status__id=1):
        order_ = Order.objects.get(user=request.user, status__base_status__id=1)
    else:
        status = Status(base_status=BaseStatus.objects.get(id=1), datetime=datetime.now())
        status.save()
        order_ = Order(user=request.user)
        order_.save()
        order_.status.add(status)
        order_.save()
    addresses = Address.objects.filter(Q(user=request.user) | Q(user__id=1))
    return render(request, "basket.html", {"order": order_,
                                           "addresses": addresses,
                                           "payment_methods": PaymentMethod.objects.all(),
                                           "categories": Category.objects.all(),
                                           "advertisements": Advertising.objects.all()})


def basket_add(request, product_id):
    product_ = Product.objects.get(id=product_id)
    if Order.objects.filter(user=request.user, status__base_status__id=1):
        order_ = Order.objects.get(user=request.user, status__base_status__id=1)
    else:
        status = Status(base_status=BaseStatus.objects.get(id=1), datetime=datetime.now())
        status.save()
        order_ = Order(user=request.user)
        order_.save()
        order_.status.add(status)
        order_.save()

    ordered_products = order_.products.all()
    if product_ in [ordered_product.product for ordered_product in ordered_products]:
        for order_prod in ordered_products:
            if order_prod.product == product_:
                order_prod.count += 1
                order_prod.save()
                break
    else:
        ordered_product = OrderedProduct(product=product_, count=1)
        ordered_product.save()
        order_.products.add(ordered_product)
        order_.save()
    return HttpResponseRedirect(request.GET.get("path"))


def basket_create(request):
    if request.POST.get("address"):
        address = Address.objects.get(id=request.POST.get("address"))
    else:
        address = Address(user=request.user, name=request.POST.get("name"), city=request.POST.get("city"),
                          street=request.POST.get("street"), home=request.POST.get("home"),
                          flat=request.POST.get("flat"))
        address.save()

    order_ = Order.objects.get(user=request.user, status__base_status__id=1)
    order_.address = address
    order_.payment_method = PaymentMethod.objects.get(id=request.POST.get("payment_method"))
    status = Status(base_status=BaseStatus.objects.get(id=2), datetime=datetime.now())
    status.save()
    order_.status.add(status)
    order_.status.remove(order_.status.all()[0])
    order_.save()

    return HttpResponseRedirect("/profile/")


def error_500(request):
    return render(request, "error_500.html", {"categories": Category.objects.all(),

                                              "advertisements": Advertising.objects.all()})


def error_404(request, exception):
    return render(request, "error_404.html", {"categories": Category.objects.all(),
                                              "advertisements": Advertising.objects.all()})
