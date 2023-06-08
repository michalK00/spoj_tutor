from django.urls import path

from . import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('<int:task_id>/', views.single_task, name="single_task"),
    path('csv', views.spojs, name="csv"),
    path('add_records_from_csv', views.add_records_from_csv, name="add_records_from_csv")
]
