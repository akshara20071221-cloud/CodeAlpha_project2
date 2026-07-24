from django import forms
from .models import Post, Profile, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['caption', 'image']

        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "What's on your mind?",
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']

        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write something about yourself...'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment...'
            })
        }