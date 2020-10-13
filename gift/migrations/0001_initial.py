# Generated by Django 3.0.8 on 2020-10-13 04:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('request_text', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('req_type', models.CharField(choices=[('user', 'User'), ('name', 'Users/name'), ('login', 'Users/login'), ('repo', 'Rep/name'), ('readme', 'Rep/readme'), ('description', 'Rep/desc')], max_length=15)),
            ],
        ),
    ]
