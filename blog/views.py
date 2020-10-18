from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JobInvites
from .serializers import PostSerializer
from users.models import Manager
from .forms import JobInviteCreateForm
import json


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

searchList = []

def home(request):
    global searchList
    if request.method == 'GET':
        value = request.GET.get('search')
        searchList.clear()
        allUsers = User.objects.all()
        allNames = [i.username for i in allUsers]
        for i in range(len(allNames)):
            if value.lower() in allNames[i].lower():
                searchList.append(allUsers[i])
        return HttpResponseRedirect('search/')
    return HttpResponseRedirect('/')

def searchView(request):

    value = request.POST.get('search')
    searchList.clear()
    allUsers = User.objects.all()
    allNames = [i.username for i in allUsers]
    for i in range(len(allNames)):
        if value.lower() in allNames[i].lower():
            searchList.append(allUsers[i])
    

    context = {
        'searchList' : searchList
    }
    return render(request, 'blog/searchresults.html', context)

def homeView(request):
    user = request.user
    posts = []
    jsondata = []
    ismanager = False
    if request.user.is_authenticated:
        following = user.profile.following[1:].split(',')
        
        for i in following:
            if i:
                for post in Post.objects.filter(author = int(i)):
                    posts.append(post)
                    jsondata.append({'imgUrl' : post.author.profile.image.url ,'id' : post.id , 'title' : post.title , 'content' : post.content , 'author' : post.author.username, 'authorId' : post.author.id, 'date_posted' : str(post.date_posted.strftime("%d  %B  %Y")), 'postUrl' : "/post/" + str(post.id) , 'authorUrl' : "/viewprofile/"  + str(post.author.id)})
                for jobInvites in JobInvites.objects.filter(author = int(i)):
                    posts.append(jobInvites)
                    jsondata.append({'imgUrl' : post.author.profile.image.url ,'id' : post.id , 'title' : post.title , 'content' : post.content , 'author' : post.author.username, 'authorId' : post.author.id, 'date_posted' : str(post.date_posted.strftime("%d  %B  %Y")), 'postUrl' : "/joninvite/" + str(post.id) , 'authorUrl' : "/viewprofile/"  + str(post.author.id)})

        for post in Post.objects.filter(author = request.user.id):
            posts.append(post)
            jsondata.append({'imgUrl' : post.author.profile.image.url ,'id' : post.id , 'title' : post.title , 'content' : post.content , 'author' : post.author.username, 'authorId' : post.author.id, 'date_posted' : str(post.date_posted.strftime("%d  %B  %Y")), 'postUrl' : "/post/" + str(post.id) , 'authorUrl' : "/viewprofile/"  + str(post.author.id)})

        for jobInvites in JobInvites.objects.filter(author = request.user.id):
            posts.append(jobInvites)
            jsondata.append({'imgUrl' : post.author.profile.image.url ,'id' : post.id , 'title' : post.title , 'content' : post.content , 'author' : post.author.username, 'authorId' : post.author.id, 'date_posted' : str(post.date_posted.strftime("%d  %B  %Y")), 'postUrl' : "/joninvite/" + str(post.id) , 'authorUrl' : "/viewprofile/"  + str(post.author.id)})

        posts.sort(key = lambda p: p.date_posted, reverse = True)
        jsondata.sort(key = lambda p : p['date_posted'])
        ismanager = isManager(request.user)
    context = {
        'posts': posts ,
        'postsscript' : json.dumps(jsondata),
        'isManager' : ismanager
    }

    return render(request, 'blog/home.html', context)



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def isManager(user):
    return len(Manager.objects.filter(user = user)) > 0

@login_required
def createJobInvite(request):
    if request.user.is_authenticated:
        if isManager(request.user):
            
            if request.method == 'POST':
                ji = JobInvites.objects.create(title = request.POST.get('title'), content = request.POST.get('content'), tags = request.POST.get('tags'), author = request.user)
                ji.save()

                return HttpResponseRedirect("/")
            
            context = {
                'jiForm' : JobInviteCreateForm,
                'isManager' : isManager(request.user)
            }

            return render(request, 'blog/jobInviteCreate.html', context)
        else:
            return render(request, 'blog/forbidden.html')
    else:
        return HttpResponseRedirect('/login/')

@login_required
def jobInviteDetail(request, id):
    jobinvite = JobInvites.objects.get(id = id)
    jobinvite.tags = jobinvite.tags.split(',')
    isAuthor = (request.user == jobinvite.author)
    applied = str(request.user.id) in jobinvite.applicants[1:].split(',')

    context = {
        'jobinvite' : jobinvite,
        'isOwner' : isAuthor,
        'applied' : applied,
        'isManager' : isManager(request.user)
    }

    return render(request, 'blog/jobInviteDetail.html', context)

@login_required
def jobinviteUpdate(request, id):
    jobinvite = JobInvites.objects.get(id = id)
    if request.user == jobinvite.author:

        if request.method == 'POST':
            jobinvite.title = request.POST.get('title')
            jobinvite.tags = request.POST.get('tags')
            jobinvite.content = request.POST.get('content')
            jobinvite.save()

            return redirect('jobinvite-detail', id =  id)
        data = {'title' : jobinvite.title, 'tags' : jobinvite.tags, 'content' : jobinvite.content}
        form = JobInviteCreateForm(initial = data)
        context = {
            'form' : form,
            'isManager' : isManager(request.user)
        }

        return render(request, 'blog/jobUpdateView.html', context)
    else:
        return render(request, 'blog/forbidden.html')

@login_required
def jobInviteDeleteConfirm(request, id):
    jobInvite = JobInvites.objects.get(id = id)

 
    context = {
        'object': jobInvite,
        'isManager' : isManager(request.user)
        
    }
    if request.user == jobInvite.author:
        if request.method == 'POST':
            jobInvite.delete()
            return redirect('blog-home')
        return render(request, 'blog/jobInviteDeleteView.html', context)
    else:
        return render(request, 'blog/forbidden.html')


class PostList(APIView):
    def get(self, request):
        postlist = Post.objects.all()
        serialize = PostSerializer(postlist, many = True)
        return Response(serialize.data)
    
    def post(self):
        pass

@login_required
def apply(request, jId):
    jobInvite = JobInvites.objects.get(id = jId)
    jobInvite.applicants = jobInvite.applicants + str(request.user.id) + ","
    jobInvite.save()
    return redirect('jobinvite-detail' , id = jId)

def viewApplicants(request, id):
    jobInvite = JobInvites.objects.get(id = id)
    applicants = jobInvite.applicants[1:].split(',')
    ap = []
    for i in applicants:
        if i:
            ap.append(User.objects.get(id = int(i)))

    context = {
        'List' : ap,
        'isManager' : isManager(request.user)
    }

    return render(request , 'blog/viewApplicants.html', context)
