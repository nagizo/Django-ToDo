from datetime import date, datetime
from typing import Text
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import TextInput, Widget
from.models import  ToDo
from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()
# from django.contrib.auth import get_user_mode


class ToDoForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = ToDo
        fields = ('title', 'text', 'date', 'end_date','start_time', 'end_time')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_date': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        date = self.cleaned_data['date']
        end_date = self.cleaned_data['end_date']

        if end_time <= start_time and end_date <= date:
            raise forms.ValidationError(
                '終了日時が開始日時よりも後にしてください'
            )
        return end_time
        

class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER] #受信者リスト
        try:
            send_mail(subject,message,from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる
