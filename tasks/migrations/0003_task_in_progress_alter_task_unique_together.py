# Generated by Django 4.1.7 on 2023-03-03 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('tasks', '0002_task_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('owning_group', 'title')},
        ),
    ]
