from .models import Room

def get_rooms(request):
    nav_room_list = Room.objects.all()
    return {
        'nav_room_list': nav_room_list,
    }