# Generated by Django 5.0.6 on 2024-08-13 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_userinformation_address_userinformation_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='reset_password',
            field=models.CharField(default=None, max_length=16, null=True),
        ),
    ]
