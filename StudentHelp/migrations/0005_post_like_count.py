# Generated by Django 5.0.4 on 2024-05-02 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentHelp', '0004_logement_post_transport_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]
