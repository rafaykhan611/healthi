# Generated by Django 4.2.5 on 2023-10-20 07:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='Y', max_length=1)),
                ('image', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
