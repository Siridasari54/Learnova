from django import forms
from .models import Room, Topic, Message


class RoomForm(forms.ModelForm):
    topic_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. Python, Machine Learning, Web Dev...',
            'list': 'topic-suggestions'
        }),
        label='Topic'
    )

    class Meta:
        model = Room
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Give your study room a name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'What will you study here? Describe your room...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.topic:
            self.fields['topic_name'].initial = self.instance.topic.name


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'message-input',
                'rows': 2,
                'placeholder': 'Share your thoughts, questions or answers...'
            }),
        }
        labels = {
            'body': ''
        }
