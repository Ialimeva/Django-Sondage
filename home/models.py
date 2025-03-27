from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class role(models.Model):
    role_name = models.CharField(max_length=15)

class role_and_user_connex(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    roleID = models.ForeignKey(role, on_delete=models.CASCADE)