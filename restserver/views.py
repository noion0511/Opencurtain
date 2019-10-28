from django.shortcuts import render
from .models import *
from rest_framework import viewsets, status, permissions, generics, mixins
from restserver import serializers
from account.models import User, UserAuth
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, get_backends
from opencurtain.settings import AUTHENTICATION_BACKENDS as backends
import random
from django.core.mail import send_mail
from django.http import Http404


class UserDetail(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserSerializer(user)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            authcode = request.data.get('authcode')
            if email and authcode:
                auth = UserAuth.objects.get(email=email)

                if auth and auth.authcode == authcode:
                    un = University.objects.get(pk=request.data['university'])
                    fa = Faculty.objects.get(pk=request.data['faculty'])
                    de = Department.objects.get(pk=request.data['department'])

                    user = User.objects.create_user(email, request.data['username'], un, fa, de, password=request.data['password'])

                    Subscribe.objects.create(user=user, board=un.board)
                    Subscribe.objects.create(user=user, board=fa.board)
                    Subscribe.objects.create(user=user, board=de.board)
                    
                    return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        backend = get_backends()[0]
        user = backend.authenticate(request, username=request.data.get('email'), password=request.data.get('password'))
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
    
class AuthCode(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                auth = UserAuth.objects.get(email=email)
                if auth:
                    auth.delete()
            except:
                pass
            
            authcode = str(random.randint(1000,9999))
            auth = UserAuth.objects.create(email=email, authcode=authcode)
            auth.save()
            send_mail('회원가입 인증 코드입니다', '인증코드는 ' + authcode + '입니다.', 'auth@hoony.org', [email], fail_silently=False)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class AuthCheck(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        authcode = request.data.get('authcode')
        
        if email and authcode:
            auth = UserAuth.objects.get(email=email)
            
            if auth and auth.authcode == str(authcode):
                return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = serializers.SubscribeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = serializers.BoardSerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = serializers.FacultySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = serializers.PostsSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user == None or user.is_anonymous:
            raise Http404
        serializer.save(user=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user == None or user.is_anonymous:
            raise Http404
        serializer.save(user=user)

