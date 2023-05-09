from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *


urlpatterns = [
    path('request_for_friendship', RequestForFriendship.as_view(), name='req_for_frd'),
    path('accept', AcceptRequestView.as_view(), name='accept'),
    path('refuse', RefuseRequestView.as_view(), name='refuse'),
    path('outgoing', OutgoingRequestsView.as_view(), name='outgoing'),
    path('incoming', IncomingRequestsView.as_view(), name='incoming'),
    path('friends', ShowFriendView.as_view(), name='friends'),
    path('delete_friend', DeleteFromFriendsView.as_view(), name='delete_friend'),
    path('check_status', CheckStatusView.as_view(), name='check_status'),
    path('index', IndexView.as_view(), name='index')
]