from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks'),
    path('<int:task_id>/', views.single_task, name="single_task"),
]
