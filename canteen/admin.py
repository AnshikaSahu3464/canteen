from django.contrib import admin
from canteen.models import (
    Category, MenuItem, Ingredient,
    Order, OrderItem, Cart, CartItem
)

admin.site.site_header = "Canteen Management System"
admin.site.site_title = "Canteen Admin"
admin.site.index_title = "Welcome to Canteen Admin Panel"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price',
        'stock_quantity', 'is_available', 'is_veg', 'is_packed'
    ]
    list_filter = ['category', 'is_available', 'is_veg', 'is_packed']
    search_fields = ['name', 'description']
    list_per_page = 10
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'price')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Stock', {
            'fields': ('stock_quantity', 'is_available', 'is_packed')
        }),
        ('Properties', {
            'fields': ('is_veg',)
        }),
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_stock', 'unit', 'minimum_required']
    list_editable = ['current_stock']
    list_per_page = 20


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'unit_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total_amount', 'status',
        'payment_method', 'payment_status', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'payment_status']
    search_fields = ['user__username']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['user', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_per_page = 20


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity']
    list_per_page = 20