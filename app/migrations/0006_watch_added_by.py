# Generated by Django 4.2.1 on 2023-08-21 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_watch_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]
