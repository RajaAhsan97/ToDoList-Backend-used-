from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ToDoForm(forms.Form):
    task = forms.CharField(label="Task", max_length=500)


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="Set-Password", widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label="Confirm-Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_confirmpassword(self):
        cd = self.cleaned_data

        if cd['password'] != cd['confirmpassword']:
            raise ValidationError("Your password does not match, please re-enter password again")
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)