# TODO Тут наполнять урлами.

from datetime import datetime
from django.urls import include, path, register_converter
from django.urls.converters import SlugConverter, IntConverter

from . import views


class NameOrIDConverter:
    regex = '{}|{}'.format(IntConverter.regex, SlugConverter.regex)

    def to_python(self, value):
        return views.INCOME_TYPES.get(int(value), None) if value.isdigit() else str(value)

    def to_url(self, value):
        return '%04d' % value

register_converter(NameOrIDConverter, 'name_or_id')


class IncomeTypeConverter:
    regex = '(' + ')|('.join(map(str, views.INCOME_TYPES.keys())) + ')'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value

register_converter(IncomeTypeConverter, 'income_type')


class IncomeDateConverter:
    regex = '\d{2}.\d{2}.\d{4}'

    def to_python(self, value):
        return datetime.strptime(value, '%d.%m.%Y').date()

    def to_url(self, value):
        return '%04d' % value

register_converter(IncomeDateConverter, 'income_date')


app_name = 'store'
urlpatterns = [
    path('category/<name_or_id:name_or_id>/', views.category, name='category'),
    path('product/<int:product_id>/', views.product, name='product'),

    path('incomes_list/<income_type:income_type>/', views.incomes_list, name='incomes_list'),
    path('imcomes_for_date/<income_date:admission_date>/<income_type:income_type>/', views.imcomes_for_date, name='imcomes_for_date'),

    path('income_page/<int:income_id>/', views.income_page, name='income_page'),
]
