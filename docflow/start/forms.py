#coding:utf-8


from django import forms

### Форма входа
class LoginForm(forms.Form):
    login = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-control-sm'}))
    passwd = forms.CharField(label='Пароль',widget=forms.TextInput(attrs={'type':'password', 'class':'form-control-sm'}))

