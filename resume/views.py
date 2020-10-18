from django.shortcuts import render , redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import ResumeTemplates
from users.models import Manager
# Create your views here.


def isManager(user):
    return len(Manager.objects.filter(user = user)) > 0

def resume_home(request):
    return render(request , 'resume/home.html')

def chooseTemplate(request):
    if request.method == "POST" and 'sample' in request.POST:
        print("request is ",request.POST)
        id = request.POST.get('sample')
        return HttpResponseRedirect('/resume/details/' + id)

    context = {"resume_templates" : ResumeTemplates.objects.all() , 'isManager' : isManager(request.user)}
    return render(request , 'resume/choosetemplates.html', context)

def details(request, id):
    resume = ResumeTemplates.objects.get(id = id)
    context = {'resume' : resume , 'isManager' : isManager(request.user)}
    if (request.method == 'POST' ):
        return redirect('resume-complete')
    return render(request, 'resume/detailsform.html', context)

def complete(request):
    context = {'isManager' : isManager(request.user)}
    return render(request, 'resume/complete.html' , context)