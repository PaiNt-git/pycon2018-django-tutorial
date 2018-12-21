from django.db import models

# -- справочник


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
    contractor = models.OneToOneField('DirectoryContractor', verbose_name=u"Контрагент", related_name="producer", on_delete="SET NULL")

    class Meta():
        verbose_name = u"производитель"
        verbose_name_plural = u"производители"
        app_label = "sales"

    def __str__(self):
        return 'Производитель: {}'.format(self.contractor)


class DirectoryProvider(models.Model):
    contractor = models.OneToOneField('DirectoryContractor', verbose_name=u"Контрагент", related_name="provider", on_delete="SET NULL")

    class Meta():
        verbose_name = u"поставщик"
        verbose_name_plural = u"поставщики"
        app_label = "sales"

    def __str__(self):
        return 'Поставщик: {}'.format(self.contractor)


class DirectoryNomenclature(models.Model):
    name = models.CharField(u"Наименование товара", null=False, blank=False, max_length=400)
    price = models.DecimalField(u"Цена товара", null=False, blank=False, max_digits=12, decimal_places=2)

    producers = models.ManyToManyField('DirectoryProducer', verbose_name=u"Производители", related_name="nomenclatures", )
    providers = models.ManyToManyField('DirectoryProvider', verbose_name=u"Поставщики", related_name="nomenclatures", )

    class Meta():
        verbose_name = u"номенклатура"
        verbose_name_plural = u"номенклатуры"
        app_label = "sales"
        ordering = ['name']

    def __str__(self):
        return self.name


#-- продажи


class SalesUser(models.Model):
    name = models.CharField(u"Имя покупателя", null=False, blank=False, max_length=400)

    class Meta():
        verbose_name = u"покупатель"
        verbose_name_plural = u"покупатели"
        app_label = "sales"
        ordering = ['name']

    def __str__(self):
        return self.name


class Sale(models.Model):
    nomenclature = models.ForeignKey(DirectoryNomenclature, verbose_name=u"Номенклатура товаров", related_name="sales", on_delete="SET NULL")
    number = models.DecimalField(u"Количество закупки", null=False, blank=False, max_digits=12, decimal_places=2)

    class Meta():
        verbose_name = u"продажа (транзакция)"
        verbose_name_plural = u"продажи"
        app_label = "sales"

    @property
    def summ(self):
        return self.nomenclature.price * self.number

    def __str__(self):
        return 'Продажа: {}, кол. {:,}, сумма {:,}'.format(self.nomenclature, self.number, self.summ)


class SaleCheck(models.Model):

    sell_to = models.ForeignKey('SalesUser', verbose_name=u"Покупатель", on_delete="SET NULL")
    selled = models.DateTimeField(verbose_name=u"Когда продано", blank=True, null=True, auto_now_add=True)

    sales = models.ManyToManyField('Sale', verbose_name=u"Закупка", related_name="sale_check")
    summ = models.DecimalField(u"Сумма закупки", null=False, default='0', blank=True, max_digits=12, decimal_places=2)

    class Meta():
        verbose_name = u"чек"
        verbose_name_plural = u"чеки"
        app_label = "sales"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.summ = sum([x.summ for x in self.sales.all()])
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Чек на: [{}]'.format(', '.join(map(str, self.sales.all())))[:100]
