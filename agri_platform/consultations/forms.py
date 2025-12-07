from django import forms
from .models import Question, Answer, Consultation

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'crop']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ask your farming question here...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Provide detailed information about your problem',
                'rows': 5
            }),
            'crop': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your expertise and help this farmer...',
                'rows': 4
            })
        }


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['consultation_type', 'topic', 'description', 'scheduled_date', 'duration_hours', 'location']
        widgets = {
            'consultation_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Maize Pest Management'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your farming challenge in detail',
                'rows': 4
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'step': '0.5'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your farm location or office address'
            })
        }