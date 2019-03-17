from django.db import models


class Ticker(models.Model):
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('ticker', 'date')


class Trade(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    insider = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    last_date = models.DateField()
    transaction_type = models.CharField(max_length=100)
    owner_type = models.CharField(max_length=100)
    shares_traded = models.BigIntegerField()
    last_price = models.FloatField(default=None, blank=True, null=True)
    shares_held = models.BigIntegerField()
