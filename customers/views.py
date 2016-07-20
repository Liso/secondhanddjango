from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, get_user_model, login, logout

# Create your views here.
def registerView(request, context={}):
    logout(request)
    if request.user.is_authenticated():
        return redirect('listing')

    return render_to_response('customers/register.html', context, context_instance=RequestContext(request))

def loginView(request):
    if request.user.is_authenticated():
        return redirect('listing')
    return render_to_response('customers/login.html', {}, context_instance=RequestContext(request))
