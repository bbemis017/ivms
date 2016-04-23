from django.shortcuts import render, HttpResponseRedirect
from django.template import Context
from accounts.models import *
from chat.models import *
from config.constants import *
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required


def test(request):
    return render(request,'html/test.html',locals())

def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/accounts/signup")

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

@login_required
def manage(request):

    chatToUser = ChatToUser.objects.filter(user=request.user)
    account = Accounts.objects.get(user=request.user)

    variables = { 'chatToUser' : chatToUser , 'account' : account, 'user' : request.user }

    if 'editBtn' in request.POST:
        #user has clicked on edit
        variables['editInfo'] = True
        return render(request,"html/dashboard.html", variables)

    elif 'updateBtn' in request.POST:

        username = request.POST.get('user_name')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        voice = request.POST.get('voice')

        result = account.update(voice,firstname,lastname)

        if isinstance(result,bool) and result:
            print "success"
            variables['editInfo'] = False
        else:
            print "failure"
            variables['editInfo'] = True
            variables['errorlist'] = result
            print result
            return render(request,"html/dashboard.html",variables)

    elif 'createRoomBtn' in request.POST:

        title = request.POST.get('room_name')
        result = ChatRoom.create(request.user, title)

        if not isinstance(result,ChatRoom):
            print "failure"
            print result
            variables['errorlist'] = result
            return render(request,"html/dashboard.html", variables)
        else:
            return HttpResponseRedirect("/chat/" + result.title)

    return render(request,"html/dashboard.html",variables)
