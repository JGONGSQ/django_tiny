from django.shortcuts import render

# Create your views here.


def home(request):
    c = {}
    template_name = 'webapp/index.html'

    return render(request,template_name, c)