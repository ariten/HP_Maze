from django.db import models

class Team(models.Model):
    def __str__(self):
        return self.team_name

    team_name = models.CharField(max_length=100)
