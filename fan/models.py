from django.db import models
from django.contrib.auth.models import User

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Fan(models):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
