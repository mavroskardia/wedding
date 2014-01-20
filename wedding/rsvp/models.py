from django.db import models

class Guest(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.EmailField()
	rsvpd = models.BooleanField()
	saidyes = models.BooleanField()
	total = models.IntegerField(default=0)
	additional = models.CharField(max_length=4096,blank=True)

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return '%s %s' % (self.firstname, self.lastname)