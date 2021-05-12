# Generated by Django 3.2.1 on 2021-05-08 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_key', models.CharField(max_length=255, null=True)),
                ('search_via', models.CharField(max_length=30, null=True)),
                ('search_cr', models.CharField(max_length=30, null=True)),
                ('search_cr_url', models.CharField(max_length=255, null=True)),
                ('search_verified', models.CharField(choices=[('1', 'Active'), ('0', 'Inactive')], default='0', max_length=1)),
            ],
        ),
    ]