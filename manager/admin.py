from django.contrib import admin

# Register your models here.
from manager.models import Manager_Acc,Manager_Code

admin.site.register(Manager_Acc)
admin.site.register(Manager_Code)