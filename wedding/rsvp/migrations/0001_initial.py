# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Guest'
        db.create_table(u'rsvp_guest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('rsvpd', self.gf('django.db.models.fields.BooleanField')()),
            ('saidyes', self.gf('django.db.models.fields.BooleanField')()),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('additional', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True)),
            ('song', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True)),
            ('coming_to_welcome', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'rsvp', ['Guest'])


    def backwards(self, orm):
        # Deleting model 'Guest'
        db.delete_table(u'rsvp_guest')


    models = {
        u'rsvp.guest': {
            'Meta': {'object_name': 'Guest'},
            'additional': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'coming_to_welcome': ('django.db.models.fields.BooleanField', [], {}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rsvpd': ('django.db.models.fields.BooleanField', [], {}),
            'saidyes': ('django.db.models.fields.BooleanField', [], {}),
            'song': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['rsvp']