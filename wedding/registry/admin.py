from django.contrib import admin

from registry.models import Activity, Giftor


class GiftorInline(admin.TabularInline):
    model = Giftor

    list_display = ('email', 'num_bought', 'paid',)


class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = ('name', 'unit_price', 'num_units', 'remaining_units')
    readonly_fields = ('total_cash', 'remaining_cash', )

    inlines = [GiftorInline, ]

admin.site.register(Activity, ActivityAdmin)
