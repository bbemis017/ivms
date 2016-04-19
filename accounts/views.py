from django.shortcuts import render, HttpResponseRedirect
from django.template import Context
from accounts.models import *
from django.contrib.auth import authenticate, login as django_login


def test(request):
    return render(request,'html/test.html',locals())

def signup(request):

    if request.method == "POST":

        #get information from form
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')
        voice = request.POST.get('voice')

        #if action is to login
        if action == "login":
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username,password=password)
                if user != None:
                    django_login(request, user)
                    return HttpResponseRedirect("/accounts/manage")

            #Error
            errorlist = [ Error.USER_DOES_NOT_EXIST ] 
            variables = {'errorlist' : errorlist, "action" : "login"}
            print variables

            return render(request,"html/signup.html",variables)

        elif action == "signup":
            #check if an account can be created
            result = Accounts.verify(username,password,voice)
            if isinstance(result,Accounts):
                #success
                print "success"
                return HttpResponseRedirect("/accounts/manage")
            else:
                #failure
                #account could not be created load errors into document
                print "failure"
                variables = { 'errorlist' : result, "action" : "signup"}
                print variables
                return render(request,"html/signup.html",variables)

    else:
        #not a post request load document normally
        return render(request,"html/signup.html")
