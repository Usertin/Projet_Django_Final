# Generated by Django 5.0.4 on 2024-05-07 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentHelp', '0016_delete_transportrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=20)),
                ('seats_needed', models.IntegerField()),
            ],
        ),
    ]
