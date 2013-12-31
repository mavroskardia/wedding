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