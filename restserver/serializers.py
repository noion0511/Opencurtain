from .models import *
from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    university = serializers.ReadOnlyField(source='university.username')
    faculty = serializers.ReadOnlyField(source='faculty.username')
    department = serializers.ReadOnlyField(source='department.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'university', 'faculty', 'department']


class SubscribeSerializer(serializers.ModelSerializer):
    boardname = serializers.ReadOnlyField(source='board.boardname')

    class Meta:
        model = Subscribe
        fields = ['id', 'board', 'boardname']


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'boardname']


class UniversitySerializer(serializers.ModelSerializer):
    boardname = serializers.ReadOnlyField(source='board.boardname')
    
    class Meta:
        model = University
        fields = ['id', 'universityname', 'board', 'boardname']


class FacultySerializer(serializers.ModelSerializer):
    boardname = serializers.ReadOnlyField(source='board.boardname')
    
    class Meta:
        model = Faculty
        fields = ['id', 'facultyname', 'university', 'board', 'boardname']


class DepartmentSerializer(serializers.ModelSerializer):
    boardname = serializers.ReadOnlyField(source='board.boardname')
    
    class Meta:
        model = Department
        fields = ['id', 'departmentname', 'faculty', 'university', 'board', 'boardname']


class PostsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    universityname = serializers.ReadOnlyField(source='user.university.universityname')
    boardname = serializers.ReadOnlyField(source='board.boardname')
    commentcount = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'user', 'username', 'universityname', 'board', 'boardname', 'timestamp', 'title', 'content', 'commentcount']

    def get_commentcount(self, post):
        comments = Comment.objects.filter(posts=post)
        return len(comments)



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'username', 'timestamp', 'posts', 'comment']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ImageUpload
        fields = ['posts', 'image']
