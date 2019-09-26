from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'university.universityname']


class SubscribeSerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = Subscribe
        fields = ['board']

class BoardSerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = Board
        fields = ['boardname']


class  UniversitySerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = University
        fields = ['university.universityname','board.boardname']


class FacultySerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = Faculty
        fields = ['facultyname', 'university.universityname','board.boardname']


class DepartmentSerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = Department
        fields = ['departmentname','faulty','university.universityname','board.boardname']


class PostsSerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = Posts
        fields = ['user.username','timestemp','title','content']


class CommentSerializer(serializer.HyperlinkedModelSerializer):
    class meta:
        model = Comment
        fields = ['user.usename','timestemp','posts','comment']