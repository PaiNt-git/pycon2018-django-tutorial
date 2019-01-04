from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat

class Person(models.Model):
    """Модель физ. лиц"""

    firstname = models.CharField('Имя', max_length=25)
    patronimyc = models.CharField('Отчество', max_length=25)
    lastname = models.CharField('Фамилия', max_length=25)
    address = models.CharField('Адресс', max_length=255)
    birth_date = models.DateField('Дата рожления')

    document = models.CharField('Документ', max_length=25)
    document_number = models.CharField('Номер', max_length=25)
    document_date = models.DateField('Дата выдачи')

    create_at = models.DateField('Дата создания', auto_now_add=True)
    modify_at = models.DateField('Дата модификации', auto_now=True)


    def fio(self):
        return '{} {} {}'.format(self.lastname, self.firstname, self.patronimyc, )
    fio.short_description = u'ФИО'
    fio.admin_order_field = Concat('lastname', Value(' '), 'firstname', Value(' '), 'patronimyc')

    fio_prop = property(fio)

    def __str__(self):
        return f'{self.lastname} {self.patronimyc} {self.lastname}'

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'


class Emploee(models.Model):
    """Информация о сотрудниках."""

    person = models.OneToOneField(Person, on_delete=models.PROTECT)
    position = models.CharField('Должность', max_length=100)

    def person_fio(self):
        return '{} {} {}'.format(self.person.lastname, self.person.firstname, self.person.patronimyc, )
    person_fio.short_description = u'ФИО'
    person_fio.admin_order_field = Concat('person__lastname', Value(' '), 'person__firstname', Value(' '), 'person__patronimyc')

    fio_prop = property(person_fio)

    def person_birth_date(self):
        return self.person.birth_date
    person_birth_date.short_description = u'Дата рождения'
    person_birth_date.admin_order_field = 'person__birth_date'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class AccessControl(models.Model):
    """Управление доступом."""

    NO_ACCESS = 0
    GUEST = 1
    EMPLOEE = 2
    GUARD = 8
    DIRECTOR = 9
    MAIN = 10

    ACCESS_LEVELS = (
        (NO_ACCESS, 'Нет доступа'),
        (GUEST, 'Гость'),
        (EMPLOEE, 'Сотрудник'),
        (GUARD, 'Охранник'),
        (DIRECTOR, 'Руководитель'),
        (MAIN, 'Владелец'),
    )

    person = models.OneToOneField(Person, on_delete=models.PROTECT)

    reason = models.CharField('Причина получения', max_length=255)
    pass_number = models.CharField('Номер пропуска', max_length=100)
    pass_level = models.PositiveSmallIntegerField(
        'Уровень допуска',
        choices=ACCESS_LEVELS
    )
    is_single = models.BooleanField('Разовый', default=True)

    date_open = models.DateTimeField('Дата открытия допуска')
    date_close = models.DateTimeField('Дата закрытия допуска')

    is_closed = models.BooleanField('Закрыт', default=True)

    create_at = models.DateField('Дата создания', auto_now_add=True)
    modify_at = models.DateField('Дата модификации', auto_now=True)

    def __str__(self):
        return f'{self.person_id}: {self.pass_level}'

    class Meta:
        verbose_name = 'Уровень доступа'
        verbose_name_plural = 'Уровни доступа'


class Place(models.Model):
    name = models.CharField('Название', max_length=100)
    min_access_level = models.PositiveSmallIntegerField(
        'Минимальный уровень доступа',
        choices=AccessControl.ACCESS_LEVELS
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Event(models.Model):
    """Регистрация наступления события доступа."""

    ALLOW = 0
    DENNY = 1

    EVENT_TYPES = (
        (ALLOW, 'Разрешено'),
        (DENNY, 'Запрещено'),
    )

    event_time = models.DateTimeField('Момент события', auto_now_add=True)
    event_type = models.PositiveSmallIntegerField(
        'Тип события',
        choices=EVENT_TYPES
    )
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    access_control = models.ForeignKey(AccessControl, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
