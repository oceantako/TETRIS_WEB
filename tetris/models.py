from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class TetrisResult(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    blockcount = models.IntegerField(default=0)
    date = models.DateTimeField()
    def __str__(self):
        return str(self.name)

