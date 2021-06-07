from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

class BoardAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

from home.models import Search_history
admin.site.register(Search_history,BoardAdmin)

from home.models import Member_info
admin.site.register(Member_info,BoardAdmin)

from home.models import Product_info
admin.site.register(Product_info,BoardAdmin)
# Register your models here.




