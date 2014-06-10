from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib import messages

from .models import Activity
from rsvp.models import Guest


class ActivityListView(View):
    template_name = 'registry/main.html'
    model = Activity

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'activities': self.model.objects.all()})


class PledgeView(View):
    summary_template_name = 'registry/pledge_summary.html'

    def post(self, request, *args, **kwargs):
        pledges = self.build_pledges(request)

        if not pledges:
            messages.warning(request,
                             'Please indicate a number of units of at least \
                             one activity before pledging.')
            return HttpResponseRedirect(reverse('registry:main'))

        grand_total = sum([t[2] for t in pledges])
        return render(request, self.summary_template_name,
                      {'pledges': pledges, 'grand_total': grand_total})

    def build_pledges(self, request):
        ret = []

        for k in request.POST:
            if k.startswith('activity_id_'):
                activity = Activity.objects.get(pk=request.POST[k])
                amount = int(request.POST.get('amount_%s' %
                             k.split('_')[-1], "0") or "0")
                if amount == 'all':
                    amount = activity.remaining_units()

                total = amount * activity.unit_price

                if amount:
                    ret.append((activity, amount, total))

        return ret


class CommitPledgeView(View):
    template_name = 'registry/commit.html'

    def post(self, request, *args, **kwargs):
    	email = request.POST.get('email', None)
    	commit_type = request.POST.get('commit_type', None)

    	if not commit_type:
    		messages.error(request, 'Could not determine how you are commiting to your pledge.')
    		return HttpResponseRedirect(reverse('registry:main'))


    	return render(request, self.template_name, {})
