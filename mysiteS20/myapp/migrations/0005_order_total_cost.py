# Generated by Django 3.0.7 on 2020-06-22 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20200621_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Total_Cost',
            field=models.PositiveIntegerField(blank=0.0, null=True),
        ),
    ]
