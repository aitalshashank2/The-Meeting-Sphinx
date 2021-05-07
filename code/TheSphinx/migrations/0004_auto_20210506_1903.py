# Generated by Django 3.1.7 on 2021-05-06 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheSphinx', '0003_auto_20210420_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='attendees_recording',
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='TheSphinx.meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
