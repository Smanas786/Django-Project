# Generated by Django 3.0.7 on 2020-08-20 14:31

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_userprofileinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='hours',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[myapp.models.validate_range]),
        ),
    ]
