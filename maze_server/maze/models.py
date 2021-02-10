from django.db import models

class Team(models.Model):
    def __str__(self):
        return "%s, score: %s" % (self.team_name, self.score)

    team_name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)


class GameStart(models.Model):

    start_time = models.DateTimeField()
    event_duration = models.IntegerField(default=15)
