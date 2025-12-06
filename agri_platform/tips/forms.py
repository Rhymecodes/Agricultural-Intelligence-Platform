from django import forms
from .models import Tip, Comment

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['title', 'explanation', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tip title',
                'maxlength': '200'
            }),
            'explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your detailed explanation here',
                'rows': 6
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 3
            })
        }