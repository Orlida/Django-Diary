from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DiaryEntry, Comment, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'diary_picture']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Entry title...'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your diary entry here...', 'rows': 10}),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write a comment...',
                'rows': 3
            }),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell something about yourself...',
                'rows': 4
            }),
        }