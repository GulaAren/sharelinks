# Generated by Django 2.0.4 on 2018-05-01 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20180502_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='link_num',
            field=models.PositiveIntegerField(),
        ),
    ]