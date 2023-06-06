from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# It's still just a concept

class Task(models.Model):
    name = models.CharField(max_length=25)
    source = models.CharField(max_length=25)
    url = models.URLField(max_length=200)
    task_content = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class UserTask(models.Model):
    task_id = models.ForeignKey(Task, related_name="user_tasks", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="user_tasks", on_delete=models.CASCADE)
    # still don't know if we're going to keep the user_solution field
    user_solution = models.CharField(max_length=1000)
    user_note = models.CharField(max_length=500)
    finished_date = models.DateTimeField()
