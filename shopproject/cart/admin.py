from django.contrib import admin

# Register your models here.
from . models import Category,Product

class cat(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,cat)

class pro(admin.ModelAdmin):
    list_display = ['name','slug','price','stocks','cdate']
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['price','stocks']
    list_per_page = 20
admin.site.register(Product,pro)