from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.tasks, name='tasks'),
    path("my_problems/", login_required(views.user_tasks), name='user_tasks'),
    path("<int:task_id>/", views.single_task, name="single_task"),
    path("my_problems/<int:user_task_id>", login_required(views.single_user_task), name="single_user_task")
]
