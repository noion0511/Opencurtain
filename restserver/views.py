from django.shortcuts import render
from .models import *
from rest_framework import viewsets, status, permissions, generics, mixins
from restserver import serializers
from account.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, get_backends
from opencurtain.settings import AUTHENTICATION_BACKENDS as backends


class UserDetail(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserSerializer(user)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            User.objects.create_user(request.data['email'], request.data['username'], request.data['university'], request.data['faculty'], request.data['department'], password=request.data['password'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        backend = get_backends()[0]
        user = backend.authenticate(request, username=request.data['email'], password=request.data['password'])
        
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = serializers.SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = serializers.BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
