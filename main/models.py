from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Posts(models.Model):
    author_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'posts'


class Authors(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    birthdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'authors'


class UsersUser(AbstractBaseUser):

    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField(null=True)
    email = models.CharField(unique=True, max_length=254)
    birthdate = models.DateField()
    password = models.CharField(max_length=128)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['birthdate','password']

    class Meta:
        managed = False
        db_table = 'users_user'