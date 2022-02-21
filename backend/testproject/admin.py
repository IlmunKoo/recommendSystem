from django.contrib import admin
from .models import TestData, Comment, Like
# Register your models here.

admin.site.register(TestData)
admin.site.register(Comment)
admin.site.register(Like)