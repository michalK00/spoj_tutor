# Generated by Django 4.2.2 on 2023-06-14 19:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0011_spoj_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="spoj",
            name="url",
        ),
    ]
