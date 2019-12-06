from django.db import models
import commodity.settings
# Create your models here.

class commodity_data(models.Model):
    arrival_date = models.DateField()
    state = models.CharField(max_length = 100)
    district = models.CharField(max_length = 100)
    market = models.CharField(max_length = 100)
    commodity = models.CharField(max_length = 100)
    variety = models.CharField(max_length = 100)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    modal_price = models.IntegerField()
    def __str__(self):
        return self.arrival_date,self.market,self.commodity


class distance_table(models.Model):
    source = models.CharField(max_length = 250)
    destination = models.CharField(max_length = 200)
    distance = models.DecimalField(max_digits=8,decimal_places=4)
    def __str__(self):
        return str(self.source,self.destination,self.distance)
    class Meta:
        unique_together=(('source','destination'),)