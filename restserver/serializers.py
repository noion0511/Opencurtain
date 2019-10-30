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
    class Meta:
        model = University
        fields = ['id', 'universityname', 'board']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'facultyname', 'university', 'board']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'departmentname', 'faculty', 'university', 'board']


class PostsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    universityname = serializers.ReadOnlyField(source='user.university.universityname')

    class Meta:
        model = Posts
        fields = ['id', 'user', 'universityname', 'board', 'timestemp', 'title', 'content']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['user', 'timestemp', 'posts', 'comment']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ImageUpload
        fields = ['posts', 'image']
