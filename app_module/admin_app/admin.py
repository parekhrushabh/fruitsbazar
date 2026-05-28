from django.contrib import admin
from app_module.admin_app import models

# Register your models here.

admin.site.register(models.comments)
admin.site.register(models.contect)
admin.site.register(models.subscribe)
admin.site.register(models.category)
# admin.site.register(models.subcategory)
admin.site.register(models.product)
admin.site.register(models.productimage)
admin.site.register(models.ProductReview)
admin.site.register(models.Notification)
admin.site.register(models.UserStatus)

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    inlines = [OrderItemInline]

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'transaction_id', 'amount', 'payment_status', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'created_at']
    search_fields = ['transaction_id', 'order__full_name']
