import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib import messages

from .models import Activity, Giftor
from rsvp.models import Guest


class ActivityListView(View):
    template_name = 'registry/main.html'
    model = Activity

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'activities': self.model.objects.all(),
            'final_pledge': request.session.get('final_pledge', {'pledges':[]})
            })


class PledgeView(View):
    summary_template_name = 'registry/pledge_summary.html'

    def post(self, request, *args, **kwargs):
        pledges = self.build_pledges(request)

        if not pledges:
            messages.warning(request,
                             'Please indicate a number of units of at least \
                             one activity before pledging.')
            return HttpResponseRedirect(reverse('registry:main'))

        grand_total = float(sum([t[2] for t in pledges]))

        request.session['final_pledge'] = {
            'grand_total': grand_total,
            'pledges': [{'id':str(p[0].id),'num':p[1]} for p in pledges]
        }

        return render(request, self.summary_template_name,
                      {'pledges': pledges, 'grand_total': grand_total})

    def build_pledges(self, request):
        ret = []

        for k in request.POST:
            if k.startswith('activity_id_'):
                activity = Activity.objects.get(pk=request.POST[k])
                amount = request.POST.get('amount_%s' % k.split('_')[-1], "0")
                if amount == 'all':
                    amount = activity.remaining_units()
                else:
                    if not amount:
                        continue

                    amount = int(amount)

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

        final_pledge = request.session['final_pledge']
        total = final_pledge['grand_total']
        pledges = final_pledge['pledges']

        for p in pledges:
            giftor = Giftor(activity_id=p['id'], num_bought=p['num'])
            giftor.save()

    	return render(request, self.template_name, {'commit_type': commit_type, 'pledges': request.session['final_pledge']})


class UpdateAjaxView(View):

    def post(self, request, *args, **kwargs):
        activities = {}

        for key in request.POST:
            if key.startswith('activity_id_'):
                activityid = request.POST[key]
                activity = Activity.objects.get(pk=activityid)
                num = request.POST.get('amount_' + activityid, '0')

                if num == 'all':
                    num = activity.remaining_units()

                num = 0 if not num else int(num)

                if num > 0:
                    activities[activity.name] = (num, float(num * activity.unit_price))

        itemtotal = sum([activities[k][0] for k in activities])
        pledgetotal = sum([activities[k][1] for k in activities])

        activities['numitems'] = len(activities)
        activities['pledgetotal'] = pledgetotal
        activities['itemtotal'] = itemtotal
        request.session['pledges'] = activities

        return HttpResponse(json.dumps(activities))
