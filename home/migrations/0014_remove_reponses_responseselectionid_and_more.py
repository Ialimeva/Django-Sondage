# Generated by Django 5.1.6 on 2025-04-12 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_reponses_enqueteresponseid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reponses',
            name='responseSelectionID',
        ),
        migrations.AddField(
            model_name='reponses',
            name='responseSelectionID',
            field=models.ManyToManyField(related_name='reponses', to='home.responseselection'),
        ),
    ]
