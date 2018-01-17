# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render
from .models import Booking, Room
from django.shortcuts import get_object_or_404


# Landing page for  Aion  
def index( request ):
    todays_booking_list = Booking.objects.filter( booking_owner = request.user.pk ).filter( booking_date__gte = datetime.date.today().strftime("%Y-%m-%d") )
    context = { 
      'todays_booking_list': todays_booking_list,
    }

    return render( request, 'aion/index.html', context )
    

#===============================================================================
# Generic ViewForms for Room
# (No Form.py required for these. Direct View to Template)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class RoomCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'room.room_admin'
    model = Room
    fields = '__all__'
    
@method_decorator(login_required, name='dispatch')
class RoomUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'room.room_admin'
    model = Room
    fields = '__all__'
    
@method_decorator(login_required, name='dispatch')
class RoomDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'room.room_admin'
    model = Room
    success_url = reverse_lazy('rooms') 

from django.views import generic

# Generic List view for Rooms
@method_decorator(login_required, name='dispatch')
class RoomListView(generic.ListView):
    model=Room
    paginate_by=5
    
# Generic Model View for Room
@method_decorator(login_required, name='dispatch')
class RoomDetailView(generic.DetailView):
    model=Room

#===============================================================================
# Generic ViewForms for Bookings
@method_decorator(login_required, name='dispatch')
class BookingCreate(CreateView):
    model = Booking
    fields = '__all__'

from django.http import HttpResponseForbidden
@method_decorator(login_required, name='dispatch')
class BookingUpdate(UpdateView):
    model = Booking
    fields = '__all__'
    
    # https://stackoverflow.com/questions/11225704/how-to-restrict-editing-of-records-to-the-logged-in-user/11226230#11226230
    def dispatch(self, request, *args, **kwargs):
      handler = super(BookingUpdate, self).dispatch(request, *args, **kwargs)
      # Only allow editing if current user is owner
      if self.object.booking_owner != request.user:
          return HttpResponseForbidden(u"You do not have permissions to update this reservation.")
      return handler

@method_decorator(login_required, name='dispatch')
class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('bookings')
    
    def dispatch(self, request, *args, **kwargs):
      handler = super(BookingDelete, self).dispatch(request, *args, **kwargs)
      # Only allow if current user is owner
      if self.object.booking_owner != request.user:
          return HttpResponseForbidden(u"You do not have permissions to delete this reservation.")
      return handler

# Generic List view for Bookings
@method_decorator(login_required, name='dispatch')
class BookingListView(generic.ListView):
    model=Booking
    paginate_by=5
    
# Generic Model View for Booking
@method_decorator(login_required, name='dispatch')
class BookingDetailView(generic.DetailView):
    model=Booking
    
# Create new Booking from Calendar
@method_decorator(login_required, name='dispatch')
class BookingCreateFromCal(CreateView):
    model=Booking 
    fields='__all__'
    
    # This makes the view request a 
    # different template from the other BookingCreate class
    template_name_suffix='_create_form' 

# View to manage Bookings with pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required
def manageBookings(request):
    booking_list = Booking.objects.filter( booking_owner = request.user ) #Booking.objects.all()
    paginator = Paginator(booking_list, 10)
    page = request.GET.get('page', 1)
    try:
      bookings = paginator.page(page)
    except PageNotAnInteger:
      bookings = paginator.page(1)
    except EmptyPage:
      bookings = paginator.page(paginator.num_pages)
      
    return render(request, 'labreserve/booking_manage.html', {'bookings': bookings})

# View Calendar by Room ========================================================
from django.db.models import Q

@login_required
def room_view( request, room, year, month, day ):
  
  lab_room = get_object_or_404( Room, pk=room )
  
  requested_date = datetime.datetime.strptime( year+month+day, "%Y%m%d" ).date()
  
  monday = requested_date + datetime.timedelta(days=-requested_date.weekday(), weeks=0)
  tuesday = monday + datetime.timedelta(days=+1)
  wednesday = tuesday + datetime.timedelta(days=+1)
  thursday = wednesday + datetime.timedelta(days=+1)
  friday = thursday + datetime.timedelta(days=+1)
  prev_week = monday + datetime.timedelta(days=-7)
  next_week = monday + datetime.timedelta(days=+7)
  
  booking_list = Booking.objects.filter( Q(room=lab_room),Q(booking_date__gte = monday), Q(booking_date__lte = friday) )
  
  context = { 
    'room': room,
    'room_name': lab_room,
    'monday': monday, 
    'tuesday': tuesday, # start_date + relativedelta(days=5)
    'wednesday': wednesday,
    'thursday': thursday,
    'friday': friday,
    'prev_week': prev_week.strftime("%Y/%m/%d"),
    'next_week': next_week.strftime("%Y/%m/%d"),
    'booking_list' : booking_list,
  }
  
  return render( request, 'labreserve/room.html', context )

# Google Auth Views ============================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile
from .forms import UserForm,ProfileForm

# @login_required
# def Home(request):
#     return render(request, 'home/home.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'labreserve/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
    
# Generic Model View for Profiles
# @method_decorator(login_required, name='dispatch')
# class ProfileDetailView(generic.DetailView):
#     model=Profile

# Use this view to see info about who has booked a room
@login_required
def userDetailView(request, user_id):
  user = User.objects.get(pk=user_id)
  context={ 'user' : user }
  return render(request, 'labreserve/user_detail.html', context)