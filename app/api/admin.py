from django.contrib import admin
from .models import User, Category, Product, Supplier, Customer, Order, Review, Shipping, Payment, Staff, Promotion
import openpyxl
from django.http import HttpResponse
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry


def export_logs_to_excel(modeladmin, request, queryset):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Логи действий"

    columns = ["ID", "Пользователь", "Тип действия", "Объект", "Дата и время"]
    worksheet.append(columns)

    for log_entry in queryset:
        row = [
            log_entry.id,
            log_entry.user.username,
            log_entry.get_action_flag_display(),
            log_entry.object_repr,
            log_entry.action_time.strftime("%Y-%m-%d %H:%M:%S"),
        ]
        worksheet.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="log_entries.xlsx"'
    
    workbook.save(response)
    return response

export_logs_to_excel.short_description = "Экспортировать выбранные логи в Excel"


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action_flag", "object_repr", "action_time")
    list_filter = ("action_flag", "user")
    search_fields = ("object_repr", "user__username")

    actions = [export_logs_to_excel]

    class Meta:
        verbose_name = "Журнал записи"
        verbose_name_plural = "Журнал записей"


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_per_page = 20

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 20

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_categories')  
    list_per_page = 20

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_products')  
    list_per_page = 20

    def get_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    get_products.short_description = 'Products'

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    list_per_page = 20

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'total_amount')
    list_per_page = 20

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'rating', 'review_date')
    list_per_page = 20

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'shipped_date')
    list_per_page = 20

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_date', 'amount')
    list_per_page = 20

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    list_per_page = 20

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent')
    list_per_page = 20

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Promotion, PromotionAdmin)
