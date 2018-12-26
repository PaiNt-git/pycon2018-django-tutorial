# TODO Тут наполнять урлами.

from django.urls import include, path, re_path

from . import views

app_name = 'cart'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('shipping_form/', views.shipping_form, name='shipping_form'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
]
