from django.contrib import admin

from home.models import Search_history
admin.site.register(Search_history)

from home.models import Member_info
admin.site.register(Member_info)

from home.models import Product_info
admin.site.register(Product_info)
# Register your models here.
