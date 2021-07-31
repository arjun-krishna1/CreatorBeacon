from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

import random

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}-Creator"
    
class Fan(models.Model):            
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}-Fan"

    def enter(self, event_id):
        event = Event.objects.get(id=event_id)

        if not event or not self:
            return False

        else:
            if not Entry.objects.filter(event=event, fan=self):
                entry = Entry(fan=self, event = event)
                entry.save()
            return True

class Event(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)

    status_choices = {
        "not_started": "not_started",
        "in_progress": "in_progress",
        "over": "over"}

    def __str__(self):
        return f"{self.name} by {self.creator.user.username} on {self.date}"

    def getStatus(self):
        curr_time = datetime.now().time()

        # hasn't started yet
        if curr_time < self.start:
            self.status = self.status_choices["not_started"]

        elif curr_time >= self.start and curr_time < self.end:
            self.status = self.status_choices["in_progress"]

        else:
            self.status = self.status_choices["over"]

        return self.status
        
    def chooseWinners(self):
        prizes = Prize.objects.filter(event = self)
        fan_entries = Entry.objects.filter(event = self)

        choices = random.choices(fan_entries, len(prizes))

        for i in range(len(choices)):
            entry = choices[i]
            entry.won = True
            entry.prize = prizes[i]
            entry.save()

        return choices
            

class Prize(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"{self.name} for {self.event.name} by {self.event.creator.user.username}"

class Entry(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    won = models.BooleanField(null=True)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"Entry by {self.fan.user.username} for {self.event.name}"
