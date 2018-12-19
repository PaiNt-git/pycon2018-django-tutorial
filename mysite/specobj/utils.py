# TODO Для существующей моделей, необходимо написать функции
# TODO (объект и характеристика, это модели в аппке):
# TODO
# TODO Принимает объект и возвращает все его актуальные характеристики.
# TODO Возвращает queryset c актуальными спеками на текущую дату.
# TODO Возвращает queryset объектов с актульными спеками.
# TODO Принимает объект и помечает спеки объектов как не актульные, для даты меньше указаной.
# TODO Помечать на удаление объекты у которых нет актуальных спек.
# TODO Удалять объекты которые помечены на удаление.
# TODO

import datetime

from .models import Obj, Spec


def get_actual_characteristics(obj):
    characteristics = Spec.objects.filter(link=obj).all()
    return characteristics


def get_actual_characteristics_today():
    today = datetime.date.today()
    actual_chstics = Spec.objects.filter(date=today)
    return actual_chstics


def get_actual_objects_today():
    actual_chstics = get_actual_characteristics_today()
    actual_objs = actual_chstics.select_related('link')
    return actual_objs