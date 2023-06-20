from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('add_tasks', views.add_tasks_from_csv, name="add_tasks"),
    path('', admin.site.urls),
]



