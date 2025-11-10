from .models import MoodEntry, Quote, Mood
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note']
        
        


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        help_text=None  
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        help_text=None
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
        }
        help_texts = {
            'username': None,  
            'email': None,
        }
        
        
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        
        
        
# Adding quote
class QuoteForm(forms.ModelForm):
    new_mood = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Or add a new mood'
        })
    )

    mood = forms.ModelChoiceField(
        queryset=Mood.objects.all(),
        required=False,  # make dropdown optional
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Quote
        fields = ['mood', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your quote...'
            }),
        }
