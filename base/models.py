# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Pent_User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100, default="NA")
    email = models.EmailField(default="NA")
    phone = models.CharField(max_length=15)
    place = models.CharField(max_length=200, default="NA")
    addr = models.TextField(default="NA")
    ban = models.BooleanField(default=False)
    passwd = models.CharField(max_length=200, editable=True, default="NA")
    securitycode = models.CharField(max_length=200, default="NA")
    latesttestdate = models.DateTimeField(default=datetime.datetime.now, editable=True, blank=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Test(models.Model):
    colour = models.CharField(max_length=60, default="NA")
    smell = models.CharField(max_length=150, default="NA")
    ph = models.FloatField(default=0)
    tds = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    hardness = models.FloatField(default=0)
    user = models.ForeignKey(Pent_User, on_delete=models.CASCADE)
    addeddate = models.DateTimeField(default=timezone.now)
    completiondate = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    remarks = models.TextField(default="NA")

    def __str__(self):
        return "Test (id_"+str(self.id)+")"
