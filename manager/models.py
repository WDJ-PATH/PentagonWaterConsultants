from django import forms
from django.db import models

# Create your models here.


class Manager_Acc(models.Model):
    username = models.CharField(max_length=30)
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=200)

    def create(uname, fn, ln, pwd):
        username = uname
        firstname = fn
        lastname = ln
        passwd = pwd

    def __str__(self):
        return self.username

class Manager_Code(models.Model):
    code = models.CharField(max_length=200)

