from django.db import models

class Guest(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	rsvpd = models.BooleanField()
	additional = models.CharField(max_length=4096)

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return self.name