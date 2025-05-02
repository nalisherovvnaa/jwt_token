from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
       data = request.data
       username = data['username']
       password = data['password']
       user = User.objects.create_user(username=username, password=password)
       user.save()
       return Response({"data":user.username, 'msg': "Siz ro'yxatdan o'tdingiz"})


    # def post(self, request):
    #     serializer = RegisterSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'data': serializer.data, 'msg': "siz ro'yxatdan o'tdingiz"})
    #     return Response("msg": "Xatolik", "status": 400)



class Test(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = JWTAuthentication,
    def get(self, request):
        return Response({"msg":"Nimadir"})

class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    
class Logout(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = JWTAuthentication,
    def post(self, request):
        data = request.data
        refresh = RefreshToken(data['refresh'])
        refresh.blacklist()
        return Response({
            'msg': "Tizimdan chiqdingiz"
        })


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
