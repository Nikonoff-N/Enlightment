from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator

import uuid
import base64

ROLES = [
    ('OWN','Owner'),
    ('TEA','Teacher'),
    ('STU','Students'),
]

HOST_NAME = "http://localhost:8000/"

class Guild(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        users = self.lightuser_set.all()
        return f"{self.name}: {len(users)} users"

# Create your models here.
class LightUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    role = models.CharField(max_length=3,choices=ROLES,default='OWN')
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.user:
            return f"{self.user.username} - {self.role} / {self.guild.name}"
        else:
            return f"{self.role} / {self.guild.name}"

#invite for users both teachers and students
class Invite(models.Model):
    url = models.CharField(max_length=256,blank=True,null=True)
    url_hash = models.CharField(max_length=10,unique=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    light_user = models.ForeignKey(LightUser,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        self.url_hash = self.generate_hash()
        self.url = self.create_url()
        super(Invite,self).save(*args,**kwargs)

    def generate_hash(self):
        hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
        hash_exists = Invite.objects.filter(url_hash = hash)
        while hash_exists:
            hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
            hash_exists = Invite.objects.filter(url_hash = hash)
        
        hash = hash.decode('utf-8')
        return hash
    
    def create_url(self):
        return HOST_NAME+self.url_hash


    def __str__(self) -> str:
        return f"{self.active}-{self.light_user}"
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    gender = models.BooleanField(default=True) #True = male, false = female
    photo = models.ImageField(blank=True,null=True,upload_to='monolith/files/profiles')
    light = models.OneToOneField(LightUser,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.id}: {self.name}-{self.hasUser()}"

    def hasUser(self)->str:
        user = self.light.user
        if user:
            return user.username
        else:
            return 'No user!'
    
    def delete(self, *args, **kwargs):
        self.light.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=256)
    student = models.ManyToManyField(Student)
    duration = models.IntegerField(default=60)
    guild = models.ForeignKey(Guild,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}:{self.student.count()} students"
    
    def student_list(self)->list[str]:
        return [s.name for s in self.student.all()]

class Schedule(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    day = models.IntegerField(default=0)
    time = models.ImageField(default=9)

