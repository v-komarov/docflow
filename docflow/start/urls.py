#coding:utf-8

from django.conf.urls import url, include

from docflow.start.views import StartLogin, Begin, Exit


urlpatterns = [
    url(r'begin/$', Begin.as_view()),
    url(r'exit/$', Exit),
    url(r'', StartLogin.as_view()),
]