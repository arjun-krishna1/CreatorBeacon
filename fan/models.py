from django.db import models
from django.contrib.auth.models import User

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}-Creator"
    
class Fan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Event(models.Model):
    qrcode = models.ImageField(upload_to="img")
    def __str__(self):
        return f"{self.user.username}-Fan"
