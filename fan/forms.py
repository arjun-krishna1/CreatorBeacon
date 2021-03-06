from django.forms import (
    ModelForm,
    DateField, TimeField,
    DateInput, TimeInput
)

from django import forms

from django.contrib.auth.models import User

from .models import Event, Prize

class CreateAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    username = forms.CharField(label="Username")

class DateInput(DateInput):
    # A custom widget to use the HTML5 date picker
    input_type = 'date'

class TimeInput(TimeInput):
    # A custom widget to use the HTML5 date picker
    input_type = 'time'


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["name", "date", "start", "end"]

    date = DateField(widget=DateInput)
    start = TimeField(widget=TimeInput)
    end = TimeField(widget=TimeInput)

class CreatePrizeForm(ModelForm):
    class Meta:
        model = Prize
        fields = ["name"]
