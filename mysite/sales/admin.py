from django.contrib import admin

from .models import *


admin.site.register(DirectoryContractor)
admin.site.register(DirectoryProducer)
admin.site.register(DirectoryProvider)
admin.site.register(DirectoryNomenclature)
admin.site.register(SalesUser)
admin.site.register(Sale)
admin.site.register(SaleCheck)
