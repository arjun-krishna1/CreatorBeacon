from django.db import models
from django.contrib.auth.models import User

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}-Creator"
    
class Fan(models.Model):
    def enter(self, event_id):
        event = Event.objects.get(id=event_id)

        if not event or not self:
            return False

        else:
            if not Entry.objects.filter(event=event, fan=self):
                entry = Entry(fan=self, event = event)
                entry.save()
            return True
            
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

class Prize(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"{self.name} for {self.event.name} by {self.event.creator.user.username}"

class Entry(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    won = models.BooleanField(null=True)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, null=True)
