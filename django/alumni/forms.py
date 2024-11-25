from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from .models import Alumni

class AlumniSignUpForm(UserCreationForm):
    graduation_year = forms.IntegerField()
    degree = forms.ChoiceField(choices=Alumni.DEGREE_CHOICES)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class AlumniProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    class Meta:
        model = Alumni
        fields = ['graduation_year', 'degree', 'current_position', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'graduation_year': forms.NumberInput(attrs={'min': 1900, 'max': 2099}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['degree'].choices = Alumni.DEGREE_CHOICES

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)