# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Giftor.date'
        db.add_column(u'registry_giftor', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Giftor.date'
        db.delete_column(u'registry_giftor', 'date')


    models = {
        u'registry.activity': {
            'Meta': {'object_name': 'Activity'},
            'blurb': ('django.db.models.fields.CharField', [], {'default': "'no blurb yet!'", 'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'num_units': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'})
        },
        u'registry.giftor': {
            'Meta': {'object_name': 'Giftor'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registry.Activity']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_bought': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1024'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['registry']