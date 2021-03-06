from django.db import models
from django.db.models import Sum
from django.utils import timezone

import locale
locale.setlocale(locale.LC_ALL, '' )


class Activity(models.Model):
    name = models.CharField(max_length=256)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    num_units = models.IntegerField(default=1)
    blurb = models.CharField(max_length=1024, default="no blurb yet!")
    link = models.URLField(blank=True)

    def total_cash(self):
        return self.unit_price * self.num_units

    def remaining_cash(self):
        return self.total_cash() - self.cash_received()

    def cash_received(self):
        return self.total_cash() - self.remaining_units() * self.unit_price

    def remaining_units(self):
        total_bought = self.giftor_set.all().aggregate(Sum('num_bought'))['num_bought__sum'] or 0
        return self.num_units - total_bought

    remaining_units.admin_order_field = 'num_units'

    def __unicode__(self):
        return self.name

class Giftor(models.Model):
    activity = models.ForeignKey(Activity)
    date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(blank=True)
    num_bought = models.IntegerField(max_length=1024, default=0)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s: %s (%s)' % (self.activity, self.email, self.num_bought)
