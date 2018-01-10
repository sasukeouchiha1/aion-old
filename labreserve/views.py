# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render
from .models import Booking, Room
from django.shortcuts import get_object_or_404


def index( request ):
    if( request.user.is_authenticated ):
        todays_booking_list = Booking.objects.filter( booking_owner = request.user ).filter( booking_date__gte = datetime.date.today().strftime("%Y-%m-%d") )
        context = { 
          'todays_booking_list': todays_booking_list,
        }
    
    return render( request, 'aion/index.html' )

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



#===============================================================================
# OLDER CODE STILL TO BE REFACTORED / EVALUATED
'''
from django.utils import timezone
from django.template import loader



from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages




@login_required 
def home( request ):
    todays_booking_list = Booking.objects.filter( booking_owner = request.user ).filter( booking_date__gte = datetime.date.today().strftime("%Y-%m-%d") )
    context = { 
        'todays_booking_list': todays_booking_list,
    }
    return render( request, 'labreserve/home.html', context )


@login_required 
def booking_detail( request, booking_id):
  booking = get_object_or_404( Booking, pk=booking_id )
  
  if( booking.booking_owner != request.user ):
    return HttpResponseRedirect( reverse( 'labreserve:home' ) )
  
  context = {
      'room': booking.room,
      'date': booking.booking_date.strftime('%Y-%m-%d'),
      'period': booking.booking_period,
      'booking_id': booking.id,
    }
  
  return render( request, 'labreserve/booking.html', context) 


@login_required 
def booking_new( request, room, year, month, day, period ):
  # THIS VIEW IF FOR NEW BOOKINGS ONLY
  date = datetime.date(int(year), int(month), int(day))
  
  # Is this booking already in the DB?
  bookings_in_db = Booking.objects.filter( room__room_text = room ).filter( booking_date = date ).filter( booking_period = period )
  if( len(bookings_in_db) > 0 ):
    return HttpResponseRedirect( reverse( 'labreserve:home' ) )
  
  #New Booking
  date_for_form = "%s-%s-%s" % (year, month, day)
  context = {
    'room': room,
    'date': date_for_form,
    'period': period,
    'booking_id':0,
  }
 
  return render( request, 'labreserve/booking.html', context)
  
  # Does this user have ownership?
  # if(requested_booking[0].booking_owner != request.user):
  #   return HttpResponseRedirect( reverse( 'labreserve:home' ) )
    
@login_required
def book( request, booking_id ):
  # UPDATE EXISTING BOOKING:
  if( int( booking_id ) > 0 ):
    # Get existing booking
    booking = get_object_or_404( Booking, pk=booking_id)
    
    # check ownership
    if(booking.booking_owner != request.user):
      return HttpResponse("OWNER: %s REQUEST: %s" % (booking.booking_owner, request.user))
      #return HttpResponseRedirect( reverse( 'labreserve:home' ) )
  
    # Validate FK (room)
    try:
      requested_room = Room.objects.get(room_text = request.POST['room'])
      booking.room = requested_room
      booking.booking_date = request.POST['date']
      booking.booking_client = request.POST['client']
      booking.booking_period = request.POST['period']
      booking.save()
    except:
      
      # https://stackoverflow.com/questions/31629785/how-to-send-message-to-django-form
      
      messages.add_message(request, messages.INFO, 'Hello world.')
      messages.error(request, 'Document deleted.')
      
      return HttpResponseRedirect('/labreserve/booking/detail/%s/' % booking_id)
      #return HttpResponse("Booking Error")
      #return render( request, 'labreserve/booking.html', {'error': 'error occured'})
      #return render(request, '/labreserve/booking/detail/%s/' % booking_id, {'error_message':'error'} )
      
    # TODO: Save the booking changes and return
    return HttpResponse("Try succeeded! %s" % booking_id )
  
  # NEW BOOKING:
  else:
    # TODO: Write new booking code
    return HttpResponse("You're at the new booking page! %s" % booking_id )
  


    
    
    
    
def detail(request, booking_id):
  return HttpResponse("Booking Detail: %s" % booking_id)

'''  