from django.db import models
from django.utils import timezone

#ユーザテーブル
class User(models.Model):
    name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name

#WeeklyRanking用テーブル
class WeeklyRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blockcount = models.IntegerField(default=0)
    date = models.DateTimeField()
    def __str__(self):
        return str(self.user)

#MonthlyRanking用テーブル
class MonthlyRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blockcount = models.IntegerField(default=0)
    date = models.DateTimeField()
    def __str__(self):
        return str(self.user)

#AllSeasonRanking用テーブル
class AllSeasonRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blockcount = models.IntegerField(default=0)
    date = models.DateTimeField()
    def __str__(self):
        return str(self.user)

#AllSeasonRanking用テーブル
class RankSelecter(models.Model):
    underblocks = models.IntegerField()
    rank = models.CharField(max_length=20)
    syougou = models.CharField(max_length=20)
    def __str__(self):
        return str(self.underblocks)

