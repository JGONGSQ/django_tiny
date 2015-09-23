from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def user_home(request):
    c = {}
    template_name = 'webapp/index_user.html'

    return render(request, template_name, c)