# coding:utf8
from django.contrib.auth.models import User

from django import forms
from models import Order, OrderData

class OrderDataForm(forms.ModelForm):
    theme = forms.CharField(widget=forms.Textarea, required=True, error_messages={'required': 'Введите тему руботы'})
    content = forms.CharField(widget=forms.Textarea, required=True, error_messages={'required': 'Введите содержание работы'})
    class Meta:
        model = OrderData
        exclude =['created', 'order']


class ContactsForm(forms.Form):
    email = forms.EmailField(label='e-mail', error_messages={'required': u'Введите ваш email'})
    name = forms.CharField(max_length=255, label=u'Имя и фамилия', error_messages={'required': u'Ведите имя и фамилию'})
    phone = forms.IntegerField(label=u'Телефон', error_messages={'required':'Введите телефон'})

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email.lower()
        raise forms.ValidationError(
            u'Пользователь с указанным email уже существует, пожалуйста ввудите другой email или залогиньтесь.')
