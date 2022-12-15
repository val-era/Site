from .models import Message, Photo, ToJson
from django.forms import ModelForm, TextInput, ClearableFileInput



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']

        widgets ={
            "text": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ответ',
            })
        }


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['img']

        widgets = {
            'img' : ClearableFileInput(attrs={
                "onchange": "loadFile(event)",
            })
        }


class ToJsonForm(ModelForm):
    class Meta:
        model = ToJson
        fields = ['data', 'question']

        widgets = {
            'data': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата',
        }),
            'question': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вопрос для добавления',
            })
        }
