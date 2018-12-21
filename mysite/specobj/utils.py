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


from .models import Obj, Spec


def get_actual_specs(obj, actday=None):
    specs = Spec.objects.filter(link=obj).filter(date=actday)
    return specs


def set_not_actual_specs(obj, actday=None):
    updated = Spec.objects.filter(link=obj).filter(date__lt=actday).update(is_actual=False)


def set_delobj_not_actual_specs():
    # updated = Spec.objects.filter(date__lt=today).select_related('link').update(link__is_deleted=True)
    specs = updated = Spec.objects.filter(is_actual=False).select_related('link')
    for spec in specs:
        spec.link.is_deleted = True
        spec.link.save()


def del_is_delete_obj():
    deleted = Obj.objects.filter(is_deleted=True).delete()
