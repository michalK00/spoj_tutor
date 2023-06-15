from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.task, name='tasks'),
    path('/search=<search_input>', views.task, name='search_tasks'),
    path('<int:task_id>/', views.single_task, name="single_task"),
]
