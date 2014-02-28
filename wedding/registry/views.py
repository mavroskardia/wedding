from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import View

from .models import Activity


class ActivityListView(View):
    template_name = 'registry/main.html'    
    model = Activity
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'activities': Activity.objects.all()})