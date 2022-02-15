from django.contrib import admin
from .models import *


def getFieldsModel(model):
    return ['email']

class UserAdmin(admin.ModelAdmin):
    list_display = getFieldsModel(User)

admin.site.register(User, UserAdmin)