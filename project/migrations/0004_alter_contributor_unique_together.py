# Generated by Django 5.0.6 on 2024-11-23 12:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_active_alter_contributor_project'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('project', 'user')},
        ),
    ]