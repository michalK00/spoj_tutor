from django.template.response import TemplateResponse
from django.contrib import admin
from django.urls import path

from .models import Task, Spoj, UserTask
import csv

# Register your models here.
admin.site.register(Task)
admin.site.register(Spoj)
admin.site.register(UserTask)
