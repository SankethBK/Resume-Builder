from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm , UserUpdateForm , ProfileUpdateForm , ManagerForm
from .models import Manager
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from blog.models import Post

def register(request):
    mform = ManagerForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            userr = User.objects.get(username = username)
            jobchoice = request.POST['jobchoices']
            if (jobchoice == '1'):
                 m = Manager.objects.create(user = userr , company = request.POST['company'])
                 m.save()
         

            messages.success(request , f"Your account has been created! You are now able to log in")
            return redirect('login')

    else:
        form = UserRegisterForm()
        
    return render(request , 'users/register.html' , {'form' : form , 'mform' : mform})

@login_required
def profile(request):
    if (request.method == 'POST'):
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES ,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request , f"Your account has updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request , 'users/profile.html' , context)

def viewProfile(request, id):
    
    user = User.objects.get(id = id)
    isSelf = False
    if request.user.id == id:
        isSelf = True
    
    isFollowing = False

    followers = []
    following = []

    f1 = user.profile.followers
    f2 = user.profile.following
    print(f"f1 and f2 are {f1} and {f2}")
    
    if f1 != '^':
        f1 = f1[1:].split(',')
        for i in f1:
            u = User.objects.filter(id = int(i))
            if (len(u)):
                followers.append(u[0])
            else:
                f1.remove(i)
        user.profile.followers = "^" + ','.join(f1)
    
    if f2 != '^':
        f2 = f2[1:].split(',')
        for i in f2:
            u = User.objects.filter(id = int(i))
            if (len(u)):
                following.append(u[0])
            else:
                f2.remove(i)
        user.profile.following = "^" + ','.join(f2)
    
    user.save()
    
    print(f"followers = {followers} , following = {following}")
    if request.user in followers:
        isFollowing = True
    context = {
        'user' : user,
        'posts' : Post.objects.filter(author = user).order_by('-date_posted'),
        'isSelf' : isSelf,
        'isFollowing' : isFollowing,
        'followers' : followers,
        'following' : following
        
    }
    return render(request, 'users/viewprofile.html', context)


@login_required
def followers(request, name):
    u = User.objects.get(username = name)
    followers = []
    print("followers = ", u.profile.followers)
    if u.profile.followers != "^":
        for i in u.profile.followers[1:].split(','):
            followers.append(User.objects.get(id = int(i)))
        
    context = {
        'following' : False,
        'followers' : True,
        'List' : followers
    }

    return render(request, 'users/follow.html', context)

@login_required
def following(request, name):
    u = User.objects.get(username = name)
    following = []
    if u.profile.following != "^":
        for i in u.profile.following[1:].split(','):
            following.append(User.objects.get(id = int(i)))
        
    context = {
        'following' : True,
        'followers' : False,
        'List' : following
    }

    return render(request, 'users/follow.html', context)

@login_required 
def follow(request, id):
    u = request.user
    if u.profile.following == "^":
        u.profile.following += str(id)
    else:
        u.profile.following += ( "," + str(id))
    u.save()
    u = request.user
    print(f" user {u} is updated his following is {u.profile.following}")
    u2 = User.objects.get(id = id)
    
    if u2.profile.followers == "^":
        u2.profile.followers += str(u.id)
    else:
        u2.profile.followers += ( "," + str(u.id))
    u2.save()
    print(f" user {u2} is updated his follower list is {u2.profile.followers}")
    return HttpResponseRedirect('/viewprofile/' + str(id) )

@login_required
def unfollow(request, id):
    u = request.user
    following = u.profile.following[1:].split(',')
    following.remove(str(id))
    u.profile.following = '^' + ','.join(following)
    u.save()
    u = request.user
    print(f" user {u} is updated his following is {u.profile.following}")
    u2 = User.objects.get(id = id)
    follower = u2.profile.followers[1:].split(',')
    follower.remove(str(u.id))
    u2.profile.followers = '^' + ','.join(follower)
    u2.save()
    print(f" user {u2} is updated his follower list is {u2.profile.followers}")
    return HttpResponseRedirect('/viewprofile/' + str(id) )
