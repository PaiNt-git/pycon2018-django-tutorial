from django.db import models

# TODO Модели добалять сюда.
# TODO  Необходимо сделать Django модели, которую будут покрывать логику.
# TODO
# TODO  Продавцы производят продажи.
# TODO  Продажи формируются на основе справочника номенклатуры.
# TODO  Для продаж необходим отслеживать, кем она изменена и когда.
# TODO  Для продаж формируеются чеки.
# TODO  Справочники номенлатуры формируется на основе
# TODO      справочника производителей.
# TODO      справочника справочника поставщиков.
# TODO
# TODO
# TODO  В докстрингах указать какая предпологается логика, работы с моделями.
# TODO
# TODO  Необходимо сформировать миграцию.


#-- справочник

class DirectoryContractor(models.Model):
    name = models.CharField(u"Наименование контрагента", null=False, blank=False, max_length=400)

    class Meta():
        verbose_name = u"контрагент"
        verbose_name_plural = u"контрагенты"
        app_label = "sales"
        ordering = ['name']

    def __str__(self):
        return self.name


class DirectoryProducer(models.Model):
    contractor = models.OneToOneField(DirectoryContractor, verbose_name=u"Контрагент", related_name="producer", on_delete="SET NULL")

    class Meta():
        verbose_name = u"производитель"
        verbose_name_plural = u"производители"
        app_label = "sales"

    def __str__(self):
        return 'Производитель: {}'.format(self.contractor)


class DirectoryProvider(models.Model):
    contractor = models.OneToOneField(DirectoryContractor, verbose_name=u"Контрагент", related_name="provider", on_delete="SET NULL")

    class Meta():
        verbose_name = u"поставщик"
        verbose_name_plural = u"поставщики"
        app_label = "sales"

    def __str__(self):
        return 'Поставщик: {}'.format(self.contractor)


class DirectoryNomenclature(models.Model):
    name = models.CharField(u"Наименование товара", null=False, blank=False, max_length=400)

    producers = models.ManyToManyField(DirectoryProducer, verbose_name=u"Производители", related_name="nomenclatures", )
    providers = models.ManyToManyField(DirectoryProvider, verbose_name=u"Поставщики", related_name="nomenclatures", )

    class Meta():
        verbose_name = u"номенклатура"
        verbose_name_plural = u"номенклатуры"
        app_label = "sales"
        ordering = ['name']

    def __str__(self):
        return self.name


#-- продажи


class SalesUser(models.Model):
    name = models.CharField(u"Имя юзера", null=False, blank=False, max_length=400)

    class Meta():
        verbose_name = u"юзер приложения"
        verbose_name_plural = u"юзеры приложения"
        app_label = "sales"
        ordering = ['name']

    def __str__(self):
        return self.name


class UpdatedFieldsMixin(models.Model):
    updated_by = models.ForeignKey(SalesUser, verbose_name=u"Юзер, который обновил", on_delete="SET NULL")
    updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        abstract = True


class Seller(models.Model):
    user = models.OneToOneField(DirectoryContractor, verbose_name=u"Юзер", related_name="seller", on_delete="SET NULL")

    class Meta():
        verbose_name = u"продавец"
        verbose_name_plural = u"продавцы"
        app_label = "sales"

    def __str__(self):
        return 'Продавец: {}'.format(self.user)


class Sale(UpdatedFieldsMixin, models.Model):
    nomenclatures = models.ManyToManyField(DirectoryNomenclature, verbose_name=u"Номенклатуры товаров", related_name="sales", )

    class Meta():
        verbose_name = u"продажа (транзакция)"
        verbose_name_plural = u"продажи"
        app_label = "sales"

    def __str__(self):
        return 'Товары: {}'.format(', '.join(map(str, self.nomenclatures.all())))


class Check(models.Model):
    sale = models.OneToOneField(Sale, verbose_name=u"Набор товаров (транзакция)", related_name="seller", on_delete="SET NULL")

    class Meta():
        verbose_name = u"чек"
        verbose_name_plural = u"чеки"
        app_label = "sales"

    def __str__(self):
        return 'Чек на: [{}]'.format(self.sale)
