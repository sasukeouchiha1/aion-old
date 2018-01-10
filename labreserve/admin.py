# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Room, Booking
from django.contrib.auth.models import Permission
from django.forms import ModelForm
from django.core.exceptions import ValidationError

    
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1
    
class RoomAdmin(admin.ModelAdmin):
    inlines = [BookingInline]
    
class BookingAdmin(admin.ModelAdmin):
    
    # https://stackoverflow.com/questions/32279064/set-object-permissions-so-that-only-the-user-specified-in-owner-field-can-modi
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.booking_owner == request.user

# class MyAdminModel(admin.ModelAdmin):
#     
#     #this filters all by user
#     #https://stackoverflow.com/questions/1380964/restricting-admin-model-entry)
#     def has_change_permission(self, request, obj=None):
#         return obj is None or self.get_queryset(request).filter(pk=obj.pk).count() > 0
#       
#     def get_queryset(self, request):
#         query = super(MyAdminModel, self).get_queryset(request)
#         if request.user.is_superuser:
#             return query
#         else:
#             return query.filter( booking_creator = request.user)

# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Permission)