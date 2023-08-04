from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Restaurant)
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id','Name','place','Types','Img')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id','restaurant','dishname','price','image')

# @admin.register(Restaurant)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id','First_name','Last_name','Email','Mobile_number','Password','Confirm_password']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','message')

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','user','image')

admin.site.register(Order)
admin.site.register(Reviews)
