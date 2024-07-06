from django.db import models


class HHCard(models.Model):
    id = models.AutoField(primary_key=True)
    organisation = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    salary = models.FloatField(null=True)
    city = models.CharField(max_length=500)

    def __str__(self):
        return self.position + ' в ' + self.organisation
