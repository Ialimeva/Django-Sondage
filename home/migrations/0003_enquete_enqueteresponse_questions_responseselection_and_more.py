# Generated by Django 5.1.7 on 2025-03-28 17:57

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_user_role_and_user_connex_userid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='enquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(max_length=10)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enquete', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='enqueteResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(max_length=10)),
                ('responseDateTime', models.DateField(auto_now_add=True)),
                ('validationDateTime', models.DateField()),
                ('enqueteID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enqueteResponse', to='home.enquete')),
            ],
        ),
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255, unique=True)),
                ('response_type', models.CharField(max_length=50)),
                ('enqueteID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='home.enquete')),
            ],
        ),
        migrations.CreateModel(
            name='responseSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponse', models.CharField(max_length=255)),
                ('note', models.IntegerField(max_length=10)),
                ('questionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponseSelection', to='home.questions')),
            ],
        ),
        migrations.CreateModel(
            name='reponses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_comment', models.CharField(max_length=50)),
                ('enqueteResponseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='home.enqueteresponse')),
                ('questionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='home.questions')),
                ('responseSelectionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='home.responseselection')),
            ],
        ),
    ]
