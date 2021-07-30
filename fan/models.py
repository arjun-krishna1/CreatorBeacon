from django.db import models
from django.contrib.auth.models import User

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}-Creator"
    
class Fan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}-Fan"

class Event(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name} by {self.creator.user.username} on {self.date}"
