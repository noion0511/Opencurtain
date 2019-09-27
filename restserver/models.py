import datetime
#from django.db import models
#사용자, 구독, 게시판, 학교, 학부, 학과, 게시물, 댓글

#from django.conf import settings
from django.db import models

class User(models.Model):
   username = models.CharField(max_length=100)
   email = models.EmailField()
   pw = models.CharField(max_length=100)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
   department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Board(models.Model):
   boardname = models.TextField()


class Subscribe(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class University(models.Model):
   universityname = models.TextField()
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Faculty(models.Model):
   facultyname = models.TextField()
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Department(models.Model):
   departmentname = models.TextField()
   faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Posts(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   timestemp = models.DateTimeField(auto_now_add=True)
   title = models.TextField()
   content = models.TextField()
   

class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   timestemp = models.DateTimeField(auto_now_add=True)
   posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
   comment = models.TextField()


