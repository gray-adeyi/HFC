# Generated by Django 2.2.1 on 2019-05-05 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Member'),
        ),
    ]