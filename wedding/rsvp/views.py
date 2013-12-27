from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
def rsvp_ajax(req):

    email = 'boo'

    if req.method == 'POST':
        email = req.POST['email']
        if '@' in email:
            ret = 'success %s' % email
        else:
            ret = 'failure'

    return HttpResponse(ret)

def rsvp_submit_ajax(req):

	if req.method != 'POST':
		return HttpResponse('failure')

	guestlist = []

	for name, value in req.POST:
		if name.startswith('guests'):
			guestlist.append(req.POST[name])

	return HttpResponse('acknowledged the following guests: %s' % guestlist)