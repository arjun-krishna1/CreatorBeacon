from django.forms import ModelForm
from django.contrib.auth.models import User

class CreateAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
