from shop.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from shop.admin import ProductAdmin
from tags.models import TaggedItem 

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
    search_fields = [TagInline]
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
# Register your models here.
