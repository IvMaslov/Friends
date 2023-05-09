from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from rest_framework import views, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import LoginSerializer, SignUpSerializer


body_parameters = openapi.Schema(type=openapi.TYPE_OBJECT,
                                 required=["username", "password"],
                                 properties={"username": openapi.Schema(type=openapi.TYPE_STRING), "password": openapi.Schema(type=openapi.TYPE_STRING)})

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(security=[],
                         tags=["UI"])
    def get(self, request):
        return Response(template_name="login.html")

    @swagger_auto_schema(security=[],
                         responses={202: "Authorizated", 400: "Wrong username or password"}, 
                         request_body=body_parameters,
                         tags=["Authorization"])
    def post(self, request):
        serialized_obj = LoginSerializer(data=request.data, context = { "request": self.request })
        serialized_obj.is_valid(raise_exception=True)
        user = serialized_obj.validated_data["user"]
        login(request, user)
        return Response(status=202)
    

class GetUser(views.APIView):
    @swagger_auto_schema(responses={403: "Forbidden", 200: "OK"}, tags=["Authorization"])
    def get(self, request):
        return Response(data={"username": request.user.username})
    

class SignUpView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(security=[],
                         tags=["UI"])
    def get(self, request):
        return Response(template_name="signup.html")

    @swagger_auto_schema(security=[],
                         responses={200: "OK", 400: "User already exists"},
                         request_body=body_parameters,
                         tags=["Authorization"])
    def post(self, request):
        serialized_obj = SignUpSerializer(data=request.data)
        serialized_obj.is_valid(raise_exception=True)
        serialized_obj.create(serialized_obj.validated_data)
        return Response(status=200)
    

class LogoutView(views.APIView):
    @swagger_auto_schema(responses={200: "OK", 403: "Authentication credentials were not provided"}, tags=["Authorization"])
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(redirect_to="login")
    

class MainView(views.APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(responses={302: "Redirect"},
                         tags=["UI"])
    def get(self, request):
        return HttpResponseRedirect(redirect_to='index')