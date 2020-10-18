from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from core import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login/", views.authenticating, name="login"),
    path("logout/", views.deauthenticating, name="logout"),
    path("reg/", TemplateView.as_view(template_name="reg.html"), name="reg"),
    path("reg/form", views.reg_form, name="reg_form"),
    path("product/<int:product_id>", views.product, name="product"),
    path("product/<int:product_id>/add_feedback", views.add_feedback, name="add_feedback"),
    path("catalog/<int:category_id>", views.catalog, name="catalog"),
    path("search/", views.search, name="search"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit", TemplateView.as_view(template_name="profile_edit.html"), name="profile_edit"),
    path("profile/edit/form", views.profile_edit_form, name="profile_edit_form"),
    path("order/<int:order_id>", views.order, name="order"),
    path("basket/", views.basket, name="basket"),
    path("basket/create", views.basket_create, name="basket_create"),
    path("basket/add/<int:product_id>", views.basket_add, name="basket_add"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
