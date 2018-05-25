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

@admin.register(Room)   
class RoomAdmin(admin.ModelAdmin):
    inlines = [BookingInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    
    # https://stackoverflow.com/questions/32279064/set-object-permissions-so-that-only-the-user-specified-in-owner-field-can-modi
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.booking_owner == request.user