# Generated by Django 4.2.2 on 2023-06-08 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_alter_task_spoj"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="spoj",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tasks.spoj"
            ),
        ),
    ]
