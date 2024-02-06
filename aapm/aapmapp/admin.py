from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
#from .models import dealer,UserProfile

class dealerAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role') # Add 'role' to the list_display
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups') # Add 'role' to the list_filter
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role')}), # Add 'role' to the 'Personal Info' section
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'role'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role') # Add 'role' to the search_fields
    ordering = ('username',)

    def get_queryset(self, request): 
        return dealer.objects.exclude(is_superuser=True)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'dateofbirth', 'phone', 'housename', 'pincode', 'district', 'user')
    list_filter = ('district',)
    search_fields = ('fullname', 'phone', 'pincode', 'district')
    list_per_page = 25

#admin.site.register(UserProfile, UserProfileAdmin)
#admin.site.register(dealer, dealerAdmin)



from .models import Aquarium, Pet

@admin.register(Aquarium)
class AquariumAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'location')
    list_filter = ('dealer', 'location')
    search_fields = ('name', 'location')
    list_per_page = 20

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('get_category_display', 'price', 'quantity', 'location')
    list_filter = ('dealer', 'category', 'location')
    search_fields = ('get_category_display', 'location')
    list_per_page = 20
