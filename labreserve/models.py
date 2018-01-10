# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime
from datetime import date
from django.contrib.auth.models import User

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

# Create your models here.
class Room(models.Model):
    room_text = models.CharField(max_length=10)
    room_no_of_computers = models.IntegerField(default=0)
    room_description = models.CharField(max_length=200)
    room_has_projector = models.BooleanField(default=False)
    class Meta:
        permissions = (('room_admin', 'Can Add, Edit, Delete Rooms'),)
        
    def __str__(self):
        return self.room_text
        
    # Returns the url to access a particular room instance.
    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])
        

class Booking(models.Model):
    periods = ( 
        (1, '1st Period'), 
        (2, '2nd Period'), 
        (3, '3rd Period'),
        (4, '4th Period'),
        (5, '5th Period'),
        (6, '6th Period'),
        (7, '7th Period'),
        (8, '8th Period'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_owner = models.ForeignKey(User)
    booking_date = models.DateField(('Reservation Date'))#, default=date.today )
    booking_client = models.CharField(('Reserved For'), max_length=200)
    booking_period = models.IntegerField(('Period'), choices=periods, default=1)
    
    # Prevent double booking a room on the same date / period
    class Meta:
        unique_together = [
            ("booking_date", "booking_period", "room")
        ]
        default_permissions = ('add', 'change', 'delete', 'view')
    
    # Returns the url to access a particular Booking instance.
    def get_absolute_url(self):
        return reverse('booking-detail', args=[str(self.id)])   
    
    def __str__(self):
        description = 'Reserved for %s, by %s.' % (self.booking_client, self.booking_owner)
        return description