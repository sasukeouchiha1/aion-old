from django import template

register = template.Library()

'''
This renders the appropriate cell content in the 
calendar view template for bookings by room
'''
@register.simple_tag
def period_field( booking_list, date, period, user, room ):
  
  # ex: bookings/create/?room={room}&year={year}&month={month}&day={day}&period={period}
  new_booking_link = '/labreserve/bookings/new/?room=%s&year=%s&month=%s&day=%s&period=%s' % (room, date.strftime("%Y"),date.strftime("%m"),date.strftime("%d"), period)
  
  for booking in booking_list:
    if booking.booking_date == date and booking.booking_period == period:
      if booking.booking_owner == user:
        # Slot booked by user
        return '''<div class="period">%s</div>
                  <div class="booking-text">Reserved (%s)</div>
                  <div class="booking-control">
                    <a href="%s" class="btn btn-primary btn-sm">Details</a>
                  </div>''' % (period, booking.booking_owner, booking.get_absolute_url() )
                    #<a href="/labreserve/booking/detail/%s/" class="btn btn-default">Details</a>

      else:
        # Slot booked by another user
        return '''<div class="period">%s</div>
                  <div class="booking-text">Reserved (<a href="/labreserve/user/%s">%s<a>)</div>''' % (period, booking.booking_owner.id, booking.booking_owner)

  # Slot not booked
  return '''<div class="period">%s</div>
            <div class="booking-text">Available</div>
            <div class="booking-control">
              <a class="btn btn-outline-primary btn-sm"
                href="%s">
                  Book Now
              </a>
            </div>''' % (period, new_booking_link)
            


