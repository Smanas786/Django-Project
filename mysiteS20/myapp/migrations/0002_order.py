# Generated by Django 3.0.7 on 2020-06-20 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levels', models.IntegerField(blank=True, null=True)),
                ('order_status', models.IntegerField(choices=[(0, 'Cancelled'), (1, 'Order Confirmed')], default='WS')),
                ('order_date', models.DateField()),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Student', to='myapp.Student')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='myapp.Course')),
            ],
        ),
    ]