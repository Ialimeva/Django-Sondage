from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Creation des roles
class role(models.Model):
    role_name = models.CharField(max_length=15)
    
    def __str__(self):
        return self.role_name
# Connection entre role et user
class role_and_user_connex(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'role_connex')
    roleID = models.ForeignKey(role, on_delete=models.CASCADE, related_name= 'user_connex')

    
# Creation des enquetes
class enquete(models.Model):
    code = models.CharField(max_length = 10, unique = True)
    name = models.CharField(max_length = 100, unique = True)
    description = models.CharField(max_length = 255, null= True, blank= True)
    status = models.CharField(max_length = 10)
    creation_date = models.DateField(auto_now_add = True)
    start_date = models.DateField(null= False, blank= False)
    end_date = models.DateField(null= False, blank= False)
    userID = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'enquete')
    roleID = models.ForeignKey(role, on_delete = models.CASCADE, related_name= 'enquete')
    token = models.UUIDField(default = uuid.uuid4, editable = False, unique= True)
    
    def __int__(self):
        return self.id
    
# Creation des questions
class questions(models.Model):
    question = models.CharField(max_length = 255, unique = True )
    description = models.CharField(max_length = 255, unique = True )
    enqueteID = models.ForeignKey(enquete, on_delete= models.CASCADE, related_name= 'questions')
    response_type = models.CharField(max_length = 50)
    
    def __int__(self):
        return self.enqueteID
    
# Creation des reponses
class responseSelection(models.Model):
    reponse = models.CharField(max_length = 255)
    note = models.IntegerField()
    questionID = models.ForeignKey(questions, on_delete= models.CASCADE, related_name= 'reponseSelection')
    def __str__(self):
        return self.reponse

# Creation des connections entre enquete, questions et reponses
class enqueteResponse(models.Model):
    email = models.EmailField(max_length= 50)
    token = models.UUIDField(default= uuid.uuid4, editable= False, unique= True)
    enqueteID = models.ForeignKey(enquete, on_delete= models.CASCADE, related_name= 'enqueteResponse')
    status = models.CharField(max_length= 10)
    responseDate = models.DateField(auto_now_add= True)
    validationDateTime = models.DateField(auto_now_add= True)

# Creation des reposes finals
class reponses(models.Model):
    enqueteResponseID = models.ForeignKey(enqueteResponse, on_delete= models.CASCADE, related_name= 'reponses', null= True)
    questionID = models.ForeignKey(questions, on_delete= models.CASCADE, related_name= 'reponses')
    responseSelectionID = models.ForeignKey(responseSelection, on_delete= models.CASCADE, related_name= 'reponses')
    response_comment = models.CharField(max_length= 50)
