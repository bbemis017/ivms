from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse

def test(request):
    return render(request,'html/test.html',locals())
