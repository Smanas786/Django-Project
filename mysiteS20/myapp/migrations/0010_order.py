# Generated by Django 3.0.7 on 2020-07-28 03:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levels', models.PositiveIntegerField()),
                ('order_status', models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Order Confirmed')], default=1)),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('Student', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, related_name='Student', to='myapp.Student')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='myapp.Course')),
            ],
        ),
    ]