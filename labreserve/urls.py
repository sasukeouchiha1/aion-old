from django.conf.urls import include, url

from . import views

urlpatterns = [
    # ex: labreserve/
    #url(r'^$', views.home, name='home'),
    url(r'^$', views.index, name='index'),
    # URL to manage bookings
    url(r'bookings/manage/$', views.manageBookings, name='booking_manage'),
    # URL for Room-Based Calendar View
    url(r'^room/(?P<room>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.room_view, name='room'),
]

# URLS for Rooms (Using Model Forms)
urlpatterns += [ 
    url(r'^rooms/$', views.RoomListView.as_view(), name='rooms'),
    url(r'^rooms/(?P<pk>\d+)$', views.RoomDetailView.as_view(), name='room-detail'),
    url(r'^rooms/create/$', views.RoomCreate.as_view(), name='room_create'),
    url(r'^rooms/(?P<pk>\d+)/update/$', views.RoomUpdate.as_view(), name='room_update'),
    url(r'^rooms/(?P<pk>\d+)/delete/$', views.RoomDelete.as_view(), name='room_delete'),
]

# URLS for Bookings (Using Model Forms)
urlpatterns += [
    url(r'bookings/$', views.BookingListView.as_view(), name='bookings'),
    url(r'^bookings/(?P<pk>\d+)$', views.BookingDetailView.as_view(), name='booking-detail'),
    url(r'^bookings/create/$', views.BookingCreate.as_view(), name='booking_create'),
    url(r'^bookings/(?P<pk>\d+)/update/$', views.BookingUpdate.as_view(), name='booking_update'),
    url(r'^bookings/(?P<pk>\d+)/delete/$', views.BookingDelete.as_view(), name='booking_delete'),
    # New Booking from Calendar View
    url(r'^bookings/new/$', views.BookingCreateFromCal.as_view(), name='booking_create_from_cal'),
]

# Google Auth URLS ===========================================================
urlpatterns += [
    url(r'^profile/$', views.update_profile, name='edit-profile'),
    # url(r'^profile/(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name='view-profile'),
    url(r'^account/logout/$', views.Logout),
    url(r'^user/(?P<user_id>\d+)/$', views.userDetailView, name='view-profile'),
]