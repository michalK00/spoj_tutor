from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# It's still just a concept
# These were not migrated yet

class Task(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, max_length=11)
    name = models.CharField(max_length=25)
    source = models.CharField(max_length=25)
    task_content = models.CharField(max_length=500)


class UserTask(models.Model):
    task_id = models.ForeignKey(Task)
    user_id = models.ForeignKey(User)
    user_note = models.CharField(max_length=500)
    finished_date = models.DateTimeField()
