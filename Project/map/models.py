from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
