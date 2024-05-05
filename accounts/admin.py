from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
from .models import Profile

admin.site.register(Profile)


@admin.register(Cartitems)
class CartitemsAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'color_variant', 'size_variant']
admin.site.register(Cart)
     
