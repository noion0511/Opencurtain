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
                    allboard = Board.objects.get(pk=1)
                    un = University.objects.get(pk=request.data['university'])
                    fa = Faculty.objects.get(pk=request.data['faculty'])
                    de = Department.objects.get(pk=request.data['department'])

                    user = User.objects.create_user(email, request.data['username'], un, fa, de, password=request.data['password'])

                    Subscribe.objects.create(user=user, board=allboard)
                    Subscribe.objects.create(user=user, board=un.board)
                    Subscribe.objects.create(user=user, board=fa.board)
                    Subscribe.objects.create(user=user, board=de.board)
                    auth.delete()
                    
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

class UserPostView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        posts = Posts.objects.filter(user=user)
        serializer = serializers.PostsSerializer(posts, many=True)
        return Response(serializer.data)

    
class SubscribeView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        subscribes = Subscribe.objects.filter(user=user)
        serializer = serializers.SubscribeSerializer(subscribes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        board = Board.objects.get(pk=request.data.get('board'))
        subscribe = Subscribe.objects.filter(board=board, user=user)

        if len(subscribe) == 0:
            Subscribe.objects.create(user=user, board=board)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subscribe = Subscribe.objects.get(pk=request.data.get('subscribe'))

        if user == subscribe.user:
            subscribe.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UniversityView(APIView):
    def get(self, request, *args, **kwargs):
        university = University.objects.all()
        serializer = serializers.UniversitySerializer(university, many=True)
        return Response(serializer.data)


class FacultyView(APIView):
    def get(self, request, *args, **kwargs):
        university = University.objects.get(pk=kwargs['university_id'])
        faculty = Faculty.objects.filter(university=university)
        serializer = serializers.FacultySerializer(faculty, many=True)
        return Response(serializer.data)

                  
class DepartmentView(APIView):
    def get(self, request, *args, **kwargs):
        faculty = Faculty.objects.get(pk=kwargs['faculty_id'])
        department = Department.objects.filter(faculty=faculty)
        serializer = serializers.DepartmentSerializer(department, many=True)
        return Response(serializer.data)


class AllDepartmentView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        department = Department.objects.all()
        serializer = serializers.DepartmentSerializer(department, many=True)
        return Response(serializer.data)


class PostView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        board = Board.objects.get(pk=kwargs['board_id'])
        subscribe = Subscribe.objects.filter(board=board, user=user)

        if len(subscribe) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        posts = Posts.objects.filter(board=board)
        serializer = serializers.PostsSerializer(posts, many=True)
        return Response(serializer.data)


    def delete(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        posts = Posts.objects.get(pk=request.data.get('posts'))

        if user == posts.user:
            posts.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class APostView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        board = Board.objects.get(pk=kwargs['board_id'])
        subscribe = Subscribe.objects.filter(board=board, user=user)

        if len(subscribe) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        posts = Posts.objects.get(pk=kwargs['post_id'])
        serializer = serializers.PostsSerializer(posts, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        posts = Posts.objects.get(pk=kwargs['post_id'])

        if user == posts.user:
            posts.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    
class PostWriteView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        board = Board.objects.get(pk=request.data.get('board'))
        subscribe = Subscribe.objects.filter(board=board, user=user)

        if len(subscribe) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        title = request.data.get('title')
        content = request.data.get('content')
        Posts.objects.create(user=user, board=board, title=title, content=content)
        return Response(status=status.HTTP_200_OK)


class CommentView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        posts = Posts.objects.filter(pk=kwargs['post_id'])
        subscribe = Subscribe.objects.filter(board=posts.board, user=user)

        if len(subscribe) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.get(post=post)
        serializer = serializers.CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        posts = Posts.objects.filter(pk=kwargs['post_id'])
        subscribe = Subscribe.objects.filter(board=posts.board, user=user)

        if len(subscribe) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        comment = request.data.get('comment')
        Comment.objects.create(user=user, posts=posts, comment=comment)
        return Response(status=status.HTTP_200_OK)


class CommentDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        user = request.user

        if user == None or user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        posts = Posts.objects.filter(pk=kwargs['post_id'])
        comment = Comment.objects.get(pk=kwargs['comment_id'])

        if user == posts.user or user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

