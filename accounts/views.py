from django.shortcuts import render, HttpResponseRedirect
from django.template import Context
from accounts.models import *

def test(request):
    return render(request,'html/test.html',locals())

def signup(request):

    if request.method == "POST":

        #get information from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        voice = request.POST.get('voice')

        #check if an account can be created
        result = Accounts.verify(username,password,voice)
        if isinstance(result,Accounts):
            #success
            print "success"
            return HttpResponseRedirect("/")
        else:
            #failure
            #account could not be created load errors into document
            print "failure"
            variables = { 'errorlist' : result }
            print variables
            return render(request,"html/test.html",variables)
    else:
        #not a post request load document normally
        return render(request,"html/test.html")

def manage(request):
    if 'edit' in request.POST:
        #user has clicked on edit
        editInfo = True
        varibles = {"editInfo": editInfo}
        return render(request,"html/dashboard.html", varibles)
    else:
        return render(request,"html/dashboard.html")
