# Generated by Django 4.0.6 on 2022-07-27 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_tamagotchi_pet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1),
        ),
    ]
