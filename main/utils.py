from django.contrib.auth.models import User
from enum import Enum
from datetime import datetime
from .models import *

class Status(int, Enum):
    not_friends = 0
    incoming_request = 1
    outgoing_request = 2
    friends = 3


def get_user_by_username(request):
    username = request.GET.get("username", None)
    if not username:
        return None
    username = User.objects.filter(username=username)
    if len(username) == 0:
        return None
    return username[0]

def create_friendship(sender, receiver):
    time = datetime.now()
    Friends.objects.create(user_id=sender, friend_id=receiver, time=time, status="active")
    Friends.objects.create(user_id=receiver, friend_id=sender, time=time, status="active")

