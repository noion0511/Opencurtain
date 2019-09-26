import datetime
from django.db import models
#사용자, 구독, 게시판, 학교, 학부, 학과, 게시물, 댓글

from django.conf import settings
from django.db import models

class User(models.Model):
   #def setup(self):
   #   self.user = get_user_model().objects.create_user(
   #      username="username",
   #      email="email"
   #      password="password",
   username = models.CharField(max_length=100)
   email = models.EmailField()
   pw = models.CharField(max_length=100)
   university = models.ForeignKey(Univercity, on_delete=models.CASCADE)
   faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
   department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Subscribe(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Board(models.Model):
   boardname = models.CharField(max_lengh=100)


class University(models.Model):
   universityname = models.CharField(max_lengh=100)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Faculty(models.Model):
   facultyname = models.CharField(max_lengh=100)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Department(models.Model):
   departmentname = models.CharField(max_lengh=100)
   faulty = models.ForeignKey(Faulty, on_delete=models.CASCADE)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Posts(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   timestemp = models.DateTimeField(auto_now_add=True)
   title = models.CharField(max_length=100)
   content = models.CharField(max_length=3000)
   

class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   timestemp = models.DateTimeField(auto_now_add=True)
   posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
   comment = models.CharField(max_lengh=1000)


