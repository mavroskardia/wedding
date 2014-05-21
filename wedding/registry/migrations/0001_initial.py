# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'registry_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('unit_price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('num_units', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('blurb', self.gf('django.db.models.fields.CharField')(default='no blurb yet!', max_length=1024)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'registry', ['Activity'])

        # Adding model 'Giftor'
        db.create_table(u'registry_giftor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registry.Activity'])),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsvp.Guest'])),
            ('num_bought', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1024)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'registry', ['Giftor'])


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'registry_activity')

        # Deleting model 'Giftor'
        db.delete_table(u'registry_giftor')


    models = {
        u'registry.activity': {
            'Meta': {'object_name': 'Activity'},
            'blurb': ('django.db.models.fields.CharField', [], {'default': "'no blurb yet!'", 'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'num_units': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'})
        },
        u'registry.giftor': {
            'Meta': {'object_name': 'Giftor'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registry.Activity']"}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rsvp.Guest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_bought': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1024'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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

    complete_apps = ['registry']