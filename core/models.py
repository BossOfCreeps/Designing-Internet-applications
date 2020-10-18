from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    image = models.ImageField()

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return str(self.name)


class Material(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class BaseProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField(Image)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING)
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return str(self.name)

    @property
    def rate(self):
        rate_list = []
        for feedback in Feedback.objects.filter(product=self):
            rate_list.append(feedback.rate)
        return round(sum(rate_list) / len(rate_list),1) if rate_list else "-"


class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    home = models.CharField(max_length=50)
    flat = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class BaseStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Status(models.Model):
    base_status = models.ForeignKey(BaseStatus, on_delete=models.DO_NOTHING)
    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.base_status) + " " + str(self.datetime)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return str(self.base_product.name) + " " + str(self.price)


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    @property
    def price(self):
        return self.product.price * self.count

    def __str__(self):
        return str(self.product.base_product.name) + " " + str(self.product.price) + " " + str(self.count)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderedProduct)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.ManyToManyField(Status)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def price(self):
        price_ = 0
        for product in self.products.all():
            price_ += product.price
        return price_

    def __str__(self):
        return str(self.user) + " " + str(self.status.order_by("-id")[0])


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    rate = models.IntegerField()
    images = models.ManyToManyField(Image)
    datetime = models.DateTimeField()
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)


class Advertising(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return str(self.name)
