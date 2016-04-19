from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from config.constants import Error
import json

class ChatRoom(models.Model):
    owner = models.ForeignKey(User, null=False)
    title = models.CharField(max_length=100 ,unique=True, null=False)

    @staticmethod
    def create(owner,title):
        errorlist = []
        if not isinstance(owner,User):
            errorlist.append( Error.NO_OWNER )
        if not title:
            errorlist.append( Error.NO_TITLE )
            return errorlist
        if ChatRoom.objects.filter(title=title).exists():
            errorlist.append( Error.TITLE_EXISTS )
            return errorlist
        if len(errorlist) > 0:
            return errorlist
        room = ChatRoom.objects.create(owner=owner,title=title)
        return room

    def addUser(self,user):
        errorlist = []
        if not isinstance(user,User):
            errorlist.append( Error.NO_USER)
            return errorlist
        if ChatToUser.objects.filter(room=self,user=user).exists():
            errorlist.append( Error.USER_IN_ROOM )
            return errorlist
        chatToUser = ChatToUser.objects.create(room=self,user=user)
        return chatToUser

    def removeUser(self,user):
        errorlist = []
        if not isinstance(user, User):
            errorlist.append( Error.NO_USER)
            return errorlist
        try:
            ChatToUser.objects.get(room=self,user=user).delete()
        except ChatToUser.DoesNotExist:
            errorlist.append( Error.USER_NOT_IN_ROOM )
            return errorlist

        return True

    def sendMessage(self,user,text):
        errorlist = []
        if not isinstance(user, User):
            errorlist.append( Error.NO_USER)
            print "no user"
            return errorlist
        if not text:
            errorlist.append( Error.NO_MESSAGE )
            print "no message"
            return errorlist
        if not ChatToUser.objects.filter(room=self,user=user).exists():
            print "not in room"
            errorlist.append( Error.USER_NOT_IN_ROOM )
            return errorlist
        message = Message.objects.create(room=self,user=user,text=text)
        return message

    '''
    returns a string representing an array where every three elements
    represents a different message, could also return a list of errors
    1 - senders username
    2 - time message was sent in UTC
    3 - text of actual message
    @param user requesting messages
    '''
    def getMessages(self,user):
        errorlist = []
        if not isinstance(user,User):
            errorlist.append( Error.NO_USER)
            return errorlist
        if not ChatToUser.objects.filter(room=self,user=user).exists(): 
            errorlist.append( Error.USER_NOT_IN_ROOM )
            return errorlist

        messages = Message.objects.filter(room=self)
        messageList = []
        if messages.exists():
            for message in messages:
                messageList.append( message.user.username )
                messageList.append( str( message.time ) )
                messageList.append( message.text )
        return json.dumps( messageList )



    def delete(self):

        try:
            messages = Message.objects.filter(room=self).delete()
        except Message.DoesNotExist:
            pass
        try:
            allUsers = ChatToUser.objects.filter(room=self).delete()
        except ChatToUser.DoesNotExist:
            pass
        super(ChatRoom,self).delete()

class ChatToUser(models.Model):
    room = models.ForeignKey(ChatRoom, null=False)
    user = models.ForeignKey(User, null=False)

class Message(models.Model):
    user = models.ForeignKey(User, null=False)
    room = models.ForeignKey(ChatRoom, null=False)
    time = models.DateTimeField(default=timezone.now)
    #utc timezone, broswer should convert to appropiate zone
    text = models.CharField(max_length=1000, null=False)

