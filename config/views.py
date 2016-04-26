from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse
import json

def test(request):
    return render(request,'html/test.html',locals())

def json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")
