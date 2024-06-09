# Generated by Django 5.0.6 on 2024-06-09 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=50)),
                ('nature', models.CharField(choices=[('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')], max_length=50)),
                ('status', models.CharField(choices=[('TODO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')], max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_issue', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_issue', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
    ]
