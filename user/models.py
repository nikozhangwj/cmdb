# encoding: utf-8

import json

from django.db import models

# Create your models here.
path = 'user.data.json'

def get_user():
    fhandler = open(path,'rt')
    users = json.loads(fhandler.read())
    fhandler.close()
    return users

def valid_login(username,password):
    users = get_user()
    for key,user in users.items():
        if username == user['name'] and password == user['password']:
            user['id'] = key
            return user
    return False 