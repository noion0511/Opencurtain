from django.db import models


class Board(models.Model):
    boardname = models.TextField()

    def __str__(self):   
        return self.boardname


class University(models.Model):
    universityname = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):   
        return self.universityname


class Faculty(models.Model):
    facultyname = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):   
        return self.facultyname


class Department(models.Model):
    departmentname = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):   
        return self.departmentname


from account.models import User


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + "-" + str(board)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    timestemp = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title
   

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestemp = models.DateTimeField(auto_now_add=True)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):   
        return self.comment


