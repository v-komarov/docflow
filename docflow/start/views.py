#coding:utf-8

import urllib3
import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.db import connections

from docflow.start.forms import LoginForm
from docflow.settings import AUTHSERVICE





def	GetFio(request):
    return u"{} {} {}".format(request.session['docflow']['lastname'],request.session['docflow']['firstname'],request.session['docflow']['surname'])


def	GetPhone(request):
    return u"{}".format(request.session['docflow']['phone'])


def	GetEmail(request):
    return u"{}".format(request.session['docflow']['email'])


def	GetUserKod(request):
    return u"{}".format(request.session['docflow']['id'])


def GetFirstName(request):
    return u"{}".format(request.session['docflow']['firstname'])


def GetSurName(request):
    return u"{}".format(request.session['docflow']['surname'])


def GetLastName(request):
    return u"{}".format(request.session['docflow']['lastname'])


def GetJob(request):
    return u"{}".format(request.session['docflow']['job'])





### Сохранение данных пользователя в базе
def	UserSave(user_kod,name1,name2,name3,email,phone,job):
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_UserSave2(%s,%s,%s,%s,%s,%s,%s);", [user_kod,name1,name2,name3,email,phone,job])
    cursor.close()





### Запрос центра авторизации
def AuthUser(login,password,request):

    url = "http://{}?action=user-kis&login={}&passwd={}".format(AUTHSERVICE,login,password)
    http = urllib3.PoolManager()
    r = http.request('GET',url)
    d = json.loads(r.data.decode('utf-8'))
    if d['result'] == u'ok':
        request.session['docflow'] = d
        UserSave(GetUserKod(request),GetLastName(request),GetFirstName(request),GetSurName(request),GetEmail(request),GetPhone(request),GetJob(request))
        return "access accepted"
    else:
        return "access denied"





### выход
def	Exit(request):

    try:
        del request.session['docflow']
    except:
        pass

    return HttpResponseRedirect('/')




class StartLogin(TemplateView):
    template_name = "start/login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            passwd = form.cleaned_data['passwd']
            if AuthUser(login,passwd,self.request) == 'access accepted':
                return HttpResponseRedirect('/begin/')

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        return super(StartLogin, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(StartLogin, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context




class Begin(TemplateView):
    template_name = "start/begin.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        return super(Begin, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(Begin, self).get_context_data(**kwargs)
        context['fio'] = GetFio(self.request)
        context['phone'] = GetPhone(self.request)
        context['email'] = GetEmail(self.request)
        return context
