from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from config.constants import Error
import json

# Create your models here.
class Accounts(models.Model):
    #constants
    DEFAULT_VOICE = 'UK English Female'

    #model fields
    user = models.ForeignKey(User, null=False)
    voice = models.CharField(max_length=50,default=DEFAULT_VOICE)

    @staticmethod
    def create(username,password,voice=DEFAULT_VOICE):

        if User.objects.filter(username=username).exists():
            return Error.USER_EXISTS 

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        if voice == None:
            voice = Accounts.DEFAULT_VOICE

        account = Accounts.objects.create(user=user,voice=voice)
        return account 

    @staticmethod
    def verify(username,password,voice):
        errorlist = [] 
        if username == None or username == "":
            errorlist.append( Error.NO_USERNAME )
        if password == None or password == "":
            errorlist.append( Error.NO_PASSWORD )
        if len(errorlist) > 0:
            return errorlist 
        else:
            if voice == "":
                account = Accounts.create(username,password)
            else:
                account = Accounts.create(username,password,voice)
            if account == Error.USER_EXISTS:
                errorlist.append( Error.USER_EXISTS)
                return errorlist 
            else:
                return account

    def delete(self):
        self.user.delete()
        super(Accounts,self).delete()


