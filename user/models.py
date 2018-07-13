# encoding: utf-8

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=32, null=False, default='') # => name varchar(32) not null default ''
    password = models.CharField(max_length=512, null=False, default='')
    age = models.IntegerField(null=False, default=0) # => age int not null default 0
    tel = models.CharField(max_length=32, null=False, default='')
    sex = models.BooleanField(null=False, default=True)
    create_time = models.DateTimeField(null=False)
    addr = models.CharField(max_length=120, null=False, default='')

    @classmethod
    def delete_user(cls,uid):
        return cls.objects.filter(id=uid).delete()

    def as_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'age' : self.age,
            'tel' : self.tel,
            'sex' : self.sex,
            'password' : self.password,
            'addr' : self.addr
        }



class Log_anlyze(models.Model):
    IP = models.CharField(max_length=255, null=False, default='')
    URL = models.CharField(max_length=512, null=False, default='')
    STATUS = models.CharField(max_length=32, null=False, default='')
    TIME = models.DateTimeField(null=False)