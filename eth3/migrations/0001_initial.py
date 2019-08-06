# Generated by Django 2.2.3 on 2019-08-02 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContractLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_name', models.TextField(max_length=100)),
                ('abi', models.TextField(max_length=100000)),
                ('bytecode', models.TextField(max_length=100000)),
                ('address', models.TextField(max_length=42)),
            ],
        ),
    ]