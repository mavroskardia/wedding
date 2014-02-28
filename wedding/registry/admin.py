from django.contrib import admin

from registry.models import Activity, Giftor

class GiftorInline(admin.TabularInline):
    model = Giftor
    
    list_display = ('guest', 'num_bought','paid',)
    readonly_fields = ('email',)
    
    
class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = ('name', 'unit_price', 'num_units','blurb',)
    readonly_fields = ('total_cash', 'remaining_cash', 'remaining_units',)
    
    inlines = [GiftorInline,]

admin.site.register(Activity, ActivityAdmin)