# Generated by Django 5.0.4 on 2024-04-25 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_tasks', '0002_todomodel_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='userModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='todomodel',
            name='User',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todo_tasks.usermodel'),
        ),
    ]