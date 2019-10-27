from django.db import models
from django.utils.translation import ugettext_lazy as _
from hashlib import sha1, md5
import os
from restserver.models import University, Faculty, Department
from django.contrib.auth.models import(
   BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, university, faculty, department, password=None):
        print(email, username, university, faculty, department, password)
        if not email:
            raise ValueError(_('Users must have an email address'))

        try:
            un = University.objects.get(pk=university)
            fa = Faculty.objects.get(pk=faculty)
            de = Department.objects.get(pk=department)
        except University.DoesNotExist or Faculty.DoesNotExist or Department.DoesNotExist:
            raise ValueError(_('Does not exists university'))

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            university = un,
            faculty = fa,
            department = de,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = email,
            username = username,
            university = 1,
            faculty = 1,
            department = 1,
            password = password,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


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

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):   
        return self.username

    def get_hashed_password(self, password):
        hashed = sha1(
                (self.salt + sha1(
                    (self.salt + sha1(
                        password.encode('utf8')
                    ).hexdigest()).encode('utf8')
                ).hexdigest()).encode('utf8')
            ).hexdigest()

        return hashed

    def set_password(self, raw_password):
        salt = md5(os.urandom(128)).hexdigest()[:9]

        self.salt = salt
        self.password = self.get_hashed_password(raw_password)

    def check_password(self, raw_password):
        try:
            user = User.objects.get(email=self.email)
            hashed = self.get_hashed_password(raw_password)

            if user.password == hashed:
                return True
            else:
                return False

        except User.DoesNotExist:
            return False

