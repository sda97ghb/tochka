# Generated by Django 2.1.7 on 2019-03-17 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_and_trades', '0003_auto_20190317_1705'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quote',
            unique_together={('ticker', 'date')},
        ),
    ]