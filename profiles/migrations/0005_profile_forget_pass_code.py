# Generated by Django 4.0.3 on 2022-03-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='forget_pass_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]