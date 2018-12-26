# TODO Тут наполнять урлами.

from django.urls import path, register_converter

from . import views


class EmailConverter:
    regex = '[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-z0-9-]+)*(\.[a-zA-Z]{2,4})'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%04d' % value

register_converter(EmailConverter, 'email')


app_name = 'sales'
urlpatterns = [
    path('sales/', views.sales, name='sales'),
    path('favorite/', views.favorite, name='favorite'),
    path('category_analytic/<slug:category>/<email:user_email>/', views.category_analytic, name='category_analytic'),
]
