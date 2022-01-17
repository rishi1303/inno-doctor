# Generated by Django 2.2.24 on 2022-01-15 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_records', '0003_auto_20220114_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicationstatement',
            name='description',
            field=models.TextField(help_text='give a short description!', null=True),
        ),
        migrations.AlterField(
            model_name='medicationitem',
            name='dose_amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='medicationitem',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='socialhistory',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vitalsign',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
