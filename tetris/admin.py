from django.contrib import admin
from tetris.models import User, WeeklyRanking, MonthlyRanking, AllSeasonRanking, RankSelecter

admin.site.register(User)
admin.site.register(WeeklyRanking)
admin.site.register(MonthlyRanking)
admin.site.register(AllSeasonRanking)
admin.site.register(RankSelecter)
# Register your models here.
