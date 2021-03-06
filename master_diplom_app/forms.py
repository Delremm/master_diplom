# coding:utf-8
from django.contrib.auth.models import User

from django import forms
from models import Order, OrderData


class OrderDataForm(forms.ModelForm):
    theme = forms.CharField(widget=forms.Textarea, required=True, label=u'Тема работы', error_messages={'required': u'Введите тему руботы'})
    content = forms.CharField(widget=forms.Textarea, required=True, label=u'Содержание', error_messages={'required': u'Введите содержание работы'})

    class Meta:
        model = OrderData
        exclude = ['created', 'order']

    def __init__(self, *args, **kwargs):
        super(OrderDataForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].required = True


class ContactsForm(forms.Form):
    email = forms.EmailField(label='e-mail', error_messages={'required': u'Введите ваш email'})
    name = forms.CharField(max_length=255, label=u'Имя и фамилия', error_messages={'required': u'Ведите имя и фамилию'})
    phone = forms.IntegerField(label=u'Телефон', error_messages={'required': u'Введите телефон'})

    icq = forms.CharField(label=u'ICQ', required=False, max_length=1000)
    town = forms.CharField(label=u'Город', required=False, max_length=1000)
    institute = forms.CharField(label=u'Учебное заведение', max_length=1000, required=False)
    time_to_call = forms.CharField(label=u'Удобное время для связи', required=False, max_length=1000)

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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) > 11:
            raise forms.ValidationError(u'Телефонный номер должен быть не более 11 символов.')
        return phone