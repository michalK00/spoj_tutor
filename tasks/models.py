from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Spoj(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    amount_of_difficulty_levels = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    difficulty = models.PositiveIntegerField()

    name = models.CharField(max_length=125)
    spoj = models.ForeignKey(Spoj, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'spoj')

    # blank=True <- not required in forms
    # null=True <- can be null in db
    url = models.URLField(max_length=200, blank=True, null=True)
    solution_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class UserTask(models.Model):
    task_id = models.ForeignKey(Task, related_name="user_tasks", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name="user_tasks", on_delete=models.CASCADE)
    # still don't know if we're going to keep the user_solution field
    user_solution = models.CharField(max_length=1000)
    user_note = models.CharField(max_length=500)
    finished_date = models.DateTimeField()
