from itertools import count
from django.contrib import admin ,messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models.query import QuerySet
from .models import Product ,Customer  ,Order  ,Collection ,VideoProduct ,Comment ,OrderItem

    
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title' ,'unit_price','inventory_status','collection_title' ]
    list_select_related = ['collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection' ,'last_update' ,InventoryFilter]
    actions = ['clear_inventory']
    prepopulated_fields = {'slug' : ['title']}
    autocomplete_fields = ['collection' ]
    search_fields = ['title' ]
    @admin.display(ordering='inventory')
    def inventory_status (self ,Product):
        if Product.inventory < 10:
            return 'low'
        return 'ok'

    @admin.action(description='clear inventory')
    def clear_inventory(self ,request ,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request ,
            f'{updated_count} products were successfully update',
            messages.ERROR
        )   
    def collection_title(self ,Product):
        return Product.collection.title

admin.site.register(Product,ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name' ,'last_name' , 'email' ,'membership' ]
    list_per_page = 10
    ordering = ['last_name']
    search_fields = ['first_name__istartswith' ,'last_name__istartswith' , ]

admin.site.register(Customer,CustomerAdmin)




class OrderItemInline(admin.TabularInline):
    
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'places_at', 'customer']
    def order_customer(self ,Order):
        return Order.customer

admin.site.register(Order ,OrderAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title' ,'product_count']
    search_fields = ['title']
    @admin.display(ordering='Product')
    def product_count(self, collection):
        url = (
            reverse('admin:shop_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('featured_product')
        )




admin.site.register(Collection ,CollectionAdmin)
admin.site.register(VideoProduct)
admin.site.register(Comment)

# Register your models here.
