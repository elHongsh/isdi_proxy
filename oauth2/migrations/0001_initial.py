# Generated by Django 2.2.3 on 2019-08-07 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.TextField(max_length=200)),
                ('client_secret', models.TextField(max_length=200)),
            ],
        ),
    ]
