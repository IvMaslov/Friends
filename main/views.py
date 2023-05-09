from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .utils import *

# Create your views here.

class RequestForFriendship(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 400: "User doesn't exist", 403: "Unauthorized"},
                         manual_parameters=[openapi.Parameter("username", openapi.IN_QUERY, type=openapi.TYPE_STRING)],
                         operation_description="Make request for friendship",
                         tags=["Friends"]
                         )
    def get(self, request):
        sender = request.user
        receiver = get_user_by_username(request)
        if sender.username == receiver.username:
            return Response(status=400, data={"error": "Can't send request to youself"})
        if not receiver:
            return Response(status=400, data={"error": "Wrong username"})
        
        check = Friends.objects.filter(user_id=sender, friend_id=receiver)
        if len(check) != 0:
            return Response(status=400, data={"error": "You already friends"})
        
        check = FriendRequest.objects.filter(sender_id=sender, receiver_id=receiver)
        if len(check) != 0:
            return Response(status=400, data={"error": "Request already exists"})
        
        check = FriendRequest.objects.filter(sender_id=receiver, receiver_id=sender)
        if len(check) != 0:
            create_friendship(sender, receiver)
            check = check[0]
            check.delete()
            return Response(status=200)

        FriendRequest.objects.create(sender_id=sender, receiver_id=receiver, status="wait")        

        return Response(status=200)
    

class AcceptRequestView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 400: "Wrong username", 403: "Unauthorized"},
                         manual_parameters=[openapi.Parameter("username", openapi.IN_QUERY, type=openapi.TYPE_STRING)],
                         operation_description="Accept request for friendship",
                         tags=["Friends"])
    def get(self, request):
        receiver = request.user
        sender = get_user_by_username(request)
        if not sender:
            return Response(status=400, data={"error": "Wrong username"})
        request_for_friend_set = FriendRequest.objects.filter(sender_id=sender, receiver_id=receiver)
        if len(request_for_friend_set) == 0:
            return Response(status=400, data={"error": "Not such request"})
        request_for_friend = request_for_friend_set[0]
        request_for_friend.delete()
        create_friendship(sender, receiver)
        return Response(200)
        

class RefuseRequestView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 400: "Wrong username", 403: "Unauthorized"},
                         manual_parameters=[openapi.Parameter("username", openapi.IN_QUERY, type=openapi.TYPE_STRING)],
                         operation_description="Refuse request for frienship",
                         tags=["Friends"])
    def get(self, request):
        receiver = request.user
        sender = get_user_by_username(request)
        if not sender:
            return Response(status=400, data={"error": "Wrong username"})
        request_for_friend_set = FriendRequest.objects.filter(sender_id=sender, receiver_id=receiver)
        if len(request_for_friend_set) == 0:
            return Response(status=400, data={"error": "Not such request"})
        request_for_friend = request_for_friend_set[0]
        request_for_friend.delete()
        return Response(200)
    

class OutgoingRequestsView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 403: "Unauthorized"},
                         operation_description="Return all outgoing requests",
                         tags=["Friends"])
    def get(self, request):
        outgoing = FriendRequest.objects.filter(sender_id=request.user)
        return Response({"outgoing": [{"username": user.receiver_id.username} for user in outgoing]})
    

class IncomingRequestsView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 403: "Unauthorized"},
                         operation_description="Return all incoming requests",
                         tags=["Friends"])
    def get(self, request):
        incoming = FriendRequest.objects.filter(receiver_id=request.user)
        return Response({"incoming": [{"username": user.sender_id.username} for user in incoming]})
    

class ShowFriendView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 403: "Unauthorized"},
                         operation_description="Return all friends",
                         tags=["Friends"])
    def get(self, request):
        friends = Friends.objects.filter(user_id=request.user)
        return Response({"friends": [{"username": user.friend_id.username} for user in friends]})
    

class DeleteFromFriendsView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 400: "Wrong username", 403: "Unauthorized",},
                         manual_parameters=[openapi.Parameter("username", openapi.IN_QUERY, type=openapi.TYPE_STRING)],
                         operation_description="Delete user from your friends",
                         tags=["Friends"])
    def get(self, request):
        user = request.user
        friend = get_user_by_username(request)
        if not friend:
            return Response(status=400, data={"error": "Wrong username"})
        one = Friends.objects.filter(user_id=user, friend_id=friend)
        two = Friends.objects.filter(user_id=friend, friend_id=user)
        if len(one) == 0 or len(two) == 0:
            return Response(status=400, data={"error": "You are not friends"})
        one.delete()
        two.delete()
        FriendRequest.objects.create(sender_id=friend, receiver_id=user, status="wait")
        return Response(status=200)
    

class CheckStatusView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 400: "Wrong username", 403: "Unauthorized",},
                         manual_parameters=[openapi.Parameter("username", openapi.IN_QUERY, type=openapi.TYPE_STRING)],
                         operation_description="Check status of friendship:\n0-not friends\n1-incoming request\n2-outgoing request\n3-friends",
                         tags=["Friends"])
    def get(self, request):
        user = request.user
        friend = get_user_by_username(request)
        if not friend:
            return Response(status=400, data={"error": "Wrong username"})
        check = Friends.objects.filter(user_id=user, friend_id=friend)
        if len(check) != 0:
            return Response({"status": Status.friends})
        check = FriendRequest.objects.filter(sender_id=user, receiver_id=friend)
        if len(check) != 0:
            return Response({"status": Status.outgoing_request})
        check = FriendRequest.objects.filter(sender_id=friend, receiver_id=user)
        if len(check) != 0:
            return Response({"status": Status.incoming_request})
        return Response({"status": Status.not_friends})


class IndexView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: "OK", 403: "Unauthorized", 302: "Redirect to auth", 406: "Not acceptable"},
                         tags=["UI"])
    def get(self, request):
        if type(request.user) == AnonymousUser:
            return HttpResponseRedirect(redirect_to="login")
        return Response(template_name="index.html")