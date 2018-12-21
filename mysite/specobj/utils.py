# TODO Для существующей моделей, необходимо написать функции
# TODO (объект и характеристика, это модели в аппке):
# TODO
# TODO Принимает объект и возвращает все его актуальные характеристики.+
# TODO Возвращает queryset c актуальными спеками на текущую дату.+
# TODO Возвращает queryset объектов с актульными спеками.+
# TODO Принимает объект и помечает спеки объектов как не актульные, для даты меньше указаной.
# TODO Помечать на удаление объекты у которых нет актуальных спек.
# TODO Удалять объекты которые помечены на удаление.
# TODO

import datetime

from .models import Obj, Spec


def get_actual_specs(obj):
    today = datetime.date.today()
    specs = Spec.objects.filter(link=obj).filter(date=today)
    return specs


def set_not_actual_specs(obj):
    today = datetime.date.today()
    updated = Spec.objects.filter(link=obj).filter(date__lt=today).update(is_actual=False)


def set_delobj_not_actual_specs():
    today = datetime.date.today()
    updated = Spec.objects.filter(date__lt=today).select_related('link').update(link__is_deleted=True)


def del_is_delete_obj():
    today = datetime.date.today()
    deleted = Obj.objects.filter(is_deleted=True).delete()
