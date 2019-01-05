from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from .models import *
import datetime

# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    '''
    Физические лица - Person
    Единичная запись.
    данные должны быть разделены на 2 группы. Личные данные, служебные данные
    доступные только для чтения.
    Данные о создании и изменении должны быть доступны только для чтения.

    Табличное представление
    ФИО, дату рождения, номер документа, документ, дату выдачи.

    Сортировка
    По алфавиту по фио.
    '''

    list_display = ('fio', 'birth_date', 'document_number', 'document', 'document_date')

    # ordering = ('fio_prop', )  # <class 'guards.admin.PersonAdmin'>: (admin.E033) The value of 'ordering[0]' refers to 'fio', which is not an attribute of 'guards.Person'.
    ordering = ('lastname', 'firstname', 'patronimyc')

    fieldsets = (
        ('Личные данные', {
            'fields': (
                'firstname',
                'patronimyc',
                'lastname',
                'address',
                'birth_date',
                'document',
                'document_number',
                'document_date',

            )
        }),
        ('Служебные данные', {
            'fields': (
                'create_at',
                'modify_at',
            ),
        }),
    )

    readonly_fields = ('create_at', 'modify_at', )


admin.site.register(Person, PersonAdmin)


class EmploeeAdmin(admin.ModelAdmin):
    '''
    Персонал - Emploee
    Табличное представление

    ФИО, дата рождения, должность.

    Сортировка
    по ФИО

    Единичная запись

    Должны быть доступны, личные данные, так же как, и в таблице физических лиц.
    Дополнительно должна быть указана группа, данных о персонале.
    Порядок вывода.
    Личные данные.
    Данные о персонале.
    Служебные данные.
    '''

    list_display = ('person_fio', 'person_birth_date', 'position')

    # ordering = ('fio_prop', )  # <class 'guards.admin.EmploeeAdmin'>: (admin.E033) The value of 'ordering[0]' refers to 'person_fio', which is not an attribute of 'guards.Emploee'.
    ordering = ('person__lastname', 'person__firstname', 'person__patronimyc')

    fieldsets = (
        ('Личные данные', {
            'fields': (
                'person',
            )
        }),
        ('Служебные данны', {
            'fields': (
                'position',
            ),
        }),
    )


admin.site.register(Emploee, EmploeeAdmin)


class PlaceAdmin(admin.ModelAdmin):
    '''
    Данные о местах, с уровнем доступа - Place
    Вывод уровня доступа, и названия.
    '''
    list_display = ('min_access_level', 'name', )


admin.site.register(Place, PlaceAdmin)


AccessControlAdmin_actions = []
for key, value in AccessControl.ACCESS_LEVELS:
    def set_access(self, request, queryset):
        _, _, fkey = request.POST['action'].rpartition('_a_')
        queryset.update(pass_level=fkey)
    set_access.short_description = "Проставить статус {}".format(value)
    act_key = 'set_access_a_{}'.format(key)
    set_access.__name__ = act_key
    AccessControlAdmin_actions.append(set_access)

set_closed = lambda self, req, qs: qs.update(is_closed=True)
set_closed.short_description = "Закрыть доступ"
AccessControlAdmin_actions.append(set_closed)


def set_single_today_access(self, request, queryset):
    today = datetime.date.today()
    start_dtme = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    end_dtme = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
    queryset.update(date_open=start_dtme, date_close=end_dtme)

set_single_today_access.short_description = "Разовый доступ + текущий день"
AccessControlAdmin_actions.append(set_single_today_access)


class AccessControlAdmin(admin.ModelAdmin):
    '''
    Данные об управлении доступом - AccessControl

    Табличное представление

    Номер пропуска,
    Дата выдачи,
    ФИО,
    уровень доступа,
    сроки действия или указание, что разовый,
    указание, что активный.

    должны быть реализованы действия:
    возможность установки конкретного уровня доступа, для нескольких человек.
    возможность закрытия доступа.
    возможность смены типа доступа, на разовый доступ.
    возможность смены типа доступа, на не разовый доступ и установка периода в
    рамках текущего дня.


    Единичное представление

    Группировка данных о физических лицах.
    Группировка данных о пропуске и уровне доступа.
    Служебная информация о создании записи доступна только для чтения.

    Сортировка
    по дате изменения в начале последние.
    '''

    def person__fio(self, obj):
        return '{} {} {}'.format(obj.person.lastname, obj.person.firstname, obj.person.patronimyc, )
    person__fio.short_description = u'ФИО'
    person__fio.admin_order_field = Concat('person__lastname', Value(' '), 'person__firstname', Value(' '), 'person__patronimyc')

    def close_override(self, obj):
        return obj.is_single or '{:%d.%m.%Y}-{:%d.%m.%Y}'.format(obj.date_open, obj.date_close)
    close_override.short_description = u'Сроки действия или указание, что разовый'

    def active(self, obj):
        return not obj.is_closed
    active.short_description = u'Указание, что активный'

    list_display = ('pass_number', 'person__fio', 'pass_level', 'close_override', 'active')

    ordering = ('-modify_at', )

    actions = AccessControlAdmin_actions

    fieldsets = (
        ('Группировка данных о физических лицах', {
            'fields': (
                'person',
            )
        }),
        ('Группировка данных о пропуске и уровне доступа', {
            'fields': (
                'reason',
                'pass_number',
                'pass_level',
                'is_single',
                'date_open',
                'date_close',
                'is_closed',

            ),
        }),
        ('Служебная информация о создании записи доступна только для чтения', {
            'fields': (
                'create_at',
                'modify_at',
            ),
        }),
    )

    readonly_fields = ('create_at', 'modify_at', )


admin.site.register(AccessControl, AccessControlAdmin)
