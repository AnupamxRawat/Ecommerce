# Generated by Django 4.1.7 on 2024-04-22 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_cart_cartitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email_token',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_email_verified',
        ),
    ]