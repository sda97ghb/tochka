# Generated by Django 2.1.7 on 2019-03-17 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_and_trades', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]