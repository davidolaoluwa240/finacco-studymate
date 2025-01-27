from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Session

'''
    Custom form for creating a user
'''
class CustomCreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={ "placeholder": "eg. John"}),
            "last_name": forms.TextInput(attrs={ "placeholder": "eg. Doe"}),
            "email": forms.EmailInput(attrs={"placeholder": "eg. johndoe@gmail.com"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-input rounded-md border-[rgba(28, 28, 28, 0.2)] placeholder:text-[rgba(28, 28, 28, 0.2)]"

class SettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "email_frequency"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-input rounded-md border-[rgba(28, 28, 28, 0.2)] placeholder:text-[rgba(28, 28, 28, 0.2)]"


'''
    Form for creating a session
'''
class CreateSessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={ "placeholder": "eg. Session 1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for  field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-input rounded-md border-[rgba(28, 28, 28, 0.2)] placeholder:text-[rgba(28, 28, 28, 0.2)] w-1/2"