# Generated by Django 5.1.6 on 2025-04-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_reponses_enqueteresponseid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reponses',
            name='enqueteResponseID',
        ),
        migrations.AddField(
            model_name='enqueteresponse',
            name='responses',
            field=models.ManyToManyField(related_name='enqueteResponse', to='home.reponses'),
        ),
    ]
