# Generated by Django 4.0.1 on 2024-04-05 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_attendance_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='SUBJECT',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.subject'),
            preserve_default=False,
        ),
    ]
