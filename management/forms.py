from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        # Ensure the user is not a superuser or staff
        user.is_superuser = False
        user.is_staff = False  # Set this to False if you want to restrict admin access
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={  # Changed to PasswordInput
        'class': 'form-control',
        'placeholder': 'Password'
    }))
