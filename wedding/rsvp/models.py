from django.db import models

class Guest(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField()
    rsvpd = models.BooleanField()
    saidyes = models.BooleanField()
    total = models.IntegerField(default=0)
    additional = models.CharField(max_length=4096,blank=True)
    song = models.CharField(max_length=256,blank=True)
    comments = models.CharField(max_length=4096,blank=True)
    coming_to_welcome = models.BooleanField()

    def __unicode__(self):
        return '%s %s' % (self.firstname, self.lastname)
    