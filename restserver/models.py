#사용자, 구독, 게시판, 학교, 학부, 학과, 게시물, 댓글
import datetime
from django.db import models
from django.contrib.auth.models import(
   BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import os
from hashlib import sha1, md5


class UserManager(BaseUserManager):
   def create_user(self, email, username, pw=None):
      if not email:
         raise ValueError(_('Users must have an email address'))

      user = self.model(
         email = self.normalize_email(email),
         username = username,
      )

      user.set_password(pw)
      user.save( _db, using=self)
      return user
   
   def create_superuser(self, email, username, pw):
      user = self.create_user(
         email = email,
         pw = pw,
         username = username,
      )

      user.is_superuser = True
      user.save(_db, using=self)
      return user


class Board(models.Model):
   boardname = models.TextField()


class University(models.Model):
   universityname = models.CharField(max_length=100)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Faculty(models.Model):
   facultyname = models.CharField(max_length=100)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Department(models.Model):
   departmentname = models.CharField(max_length=100)
   faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   board = models.ForeignKey(Board, on_delete=models.CASCADE)


class User(AbstractBaseUser, PermissionsMixin):
   username = models.CharField(
      verbose_name = _("Username"),
      max_length=100,
      unique = True
      )
   email = models.EmailField(
      verbose_name = _('Email address'),
      max_length = 225,
      unique = True
   )
   is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
   )
   salt = models.CharField(
        verbose_name=_('Salt'),
        max_length=10,
        blank=True
   )
   pw = models.CharField(max_length=100)
   university = models.ForeignKey(University, on_delete=models.CASCADE)
   faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
   department = models.ForeignKey(Department, on_delete=models.CASCADE)

   objects = UserManager()

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username',]

   def __str__(self):   
        return self.username

   def set_password(self, raw_password):
      salt = md5(os.urandom(128)).hexdigest()[:9]
      hashed = sha1(
            (salt + sha1(
                (salt + sha1(
                    raw_password.encode('utf8')
                ).hexdigest()).encode('utf8')
            ).hexdigest()).encode('utf8')
        ).hexdigest()

      self.salt = salt
      self.password = hashed

   def check_password(self, raw_password):
        try:
            user = User.objects.get(email=self.email)

            hashed = sha1(
                (user.salt + sha1(
                    (user.salt + sha1(
                        raw_password.encode('utf8')
                    ).hexdigest()).encode('utf8')
                ).hexdigest()).encode('utf8')
            ).hexdigest()

            if user.password == hashed:
                return True
            else:
                return False

        except User.DoesNotExist:
            return False
      


class Subscribe(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
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


