from django.forms import (
    ModelForm,
    DateField, TimeField,
    DateInput, TimeInput
)

from django.contrib.auth.models import User

from .models import Event

class CreateAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

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
