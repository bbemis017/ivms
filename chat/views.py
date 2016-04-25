from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from chat.models import *
from config.constants import Error
import json

# Create your views here.
def accessChat(request,title):
    #check if room exists
    try:
        room = ChatRoom.objects.get(title=title)
    except ChatRoom.DoesNotExist:
        print "room does not exist"
        #if chat does not exist direct user to does not exist page/create
        return HttpResponseRedirect("/accounts/manage")
    if not request.user.is_authenticated():
        #ask user to login to chat room
        return HttpResponseRedirect("/accounts/signup")
    try:
        userInRoom = ChatToUser.objects.get(room=room,user=request.user)
    except ChatToUser.DoesNotExist:
        #user does not have access to chat room
        return HttpResponseRedirect("/accounts/manage")

    variables = { 'room' : room.title, 'username' : request.user.username }

    print "success chat page"
    return render(request,'html/chat.html',variables)

'''
Accepts ajax request only, user must also be logged in
must provide a room and text for message
May return with errors from Error, if successful will return with
success
'''
@login_required
def sendMessage(request):
    if not request.is_ajax():
        #TODO:
        return HttpResponse("<html><body>Ajax only url</body></html>")

    errorlist = []
    data = {}
    
    #TODO: error check this
    roomTitle = request.POST.get('room')
    text = request.POST.get('message')

    try:
        room = ChatRoom.objects.get(title=roomTitle)
    except ChatRoom.DoesNotExist:
        errorlist.append( Error.NO_CHATROOM )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)

    #attempt to send message, check if error occured
    message = room.sendMessage(request.user,text)
    if not isinstance(message,Message):
        errorlist.append( message )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)

    return updateChat(request)

'''
Accepts an ajax request from a logged in user containing the room title 
returns a json response containing users, messages, or errors
If errors exists it will contain an array of error codes corresponding to
Error
'''
@login_required
def updateChat(request):
    if not request.is_ajax():
        #TODO:
        return HttpResponse("<html><body>Ajax only url</body></html>")

    errorlist = []
    data = {}

    #TODO: error check this
    roomTitle = request.POST.get('room')
    lastMessage = 0
    if 'lastMessage' in request.POST:
        lastMessage = request.POST.get('lastMessage')

    print lastMessage

    #check if room exists
    try:
        room = ChatRoom.objects.get(title=roomTitle)
    except ChatRoom.DoesNotExist:
        errorlist.append( Error.NO_CHATROOM )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)

    #get users in room and check if requesting user is in room
    userData = getUsers(room,request.user)
    if not isinstance(userData,list):
        errorlist.append( Error.USER_NOT_IN_ROOM )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)
    else:
        data['users'] = json.dumps( userData ) 

    #get all messages in room
    messages = room.getMessages(request.user,lastMessage)
    if not isinstance(messages,str):
        data['errors'] = json.dumps( messages )
        return JsonResponse(data)
    else:
        data['messages'] = messages

    print data
    #success 
    return JsonResponse(data)

def getUsers(room,user):
    userlist = ChatToUser.objects.filter(room=room)

    usernames = []
    match = False
    for entry in userlist:
        if entry.user == user:
            match = True
        else:
            usernames.append( entry.user.username )

    if not match:
        #TODO: error user cannot request users in a room, if they are not
        #also in that room
        return False

    return usernames

@login_required
def sendUser(request):
    if not request.is_ajax():
        #TODO:
        return HttpResponse("<html><body>Ajax only url</body></html>")

    errorlist = []
    data = {}
    
    #TODO: error check this
    roomTitle = request.POST.get('room')
    userName = request.POST.get('username')

    room = ChatRoom.objects.get(title=roomTitle)

    #attempt to send message, check if error occured
    if not userName:
        print "no user"
        errorlist.append( Error.NO_TITLE )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)
    tempUser = User.objects.filter(username=userName)
    if not tempUser.exists():
        print "failure"
        errorlist.append( Error.USER_DOES_NOT_EXIST )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)
    usernameRE = room.addUser(tempUser[0])
    if not isinstance(usernameRE,ChatToUser):
        errorlist.append( usernameRE )
        data['errors'] = json.dumps( errorlist )
        return JsonResponse(data)

    return updateChat(request)
