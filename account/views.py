from django.shortcuts import render,redirect,get_object_or_404
from .forms import ChangePasswordForm,SignupForm,EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash,logout
from .models import Profile
from movia.models import Review

# Create your views here.
def SignUp(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      first_name = form.cleaned_data.get('first_name')
      last_name = form.cleaned_data.get('last_name')
      password = form.cleaned_data.get('password')
      User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
      return redirect('edit-profile') #edit-profile page
  else:
    form = SignupForm()
  return render(request,'registration/signup.html',{'form':form})
 
@login_required    
def PasswordChange(request):
  user = request.user 
  if request.method == 'POST':
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
      new_password = form.cleaned_data.get('new_password')
      user.set_password(new_password)
      user.save()
      update_session_auth_hash(request,user)
      return redirect('login') 
  else:
    form = ChangePasswordForm(instance=user)
  return render(request,'registration/change_password.html',{'form':form})

def PasswordChangeDone(request):
  return render(request,'registration/change_password_done.html')



@login_required
def EditProfile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile',username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)
        
    return render(request, 'edit-profile.html', {'form': form,'profile':profile})
      
def logout_view(request):
  logout(request)
  return redirect('login')


def user_profile(request,username):
  user = get_object_or_404(User,username=username)
  profile = Profile.objects.get(user=user)
  watched_count = profile.watched.all().count()
  watchlist_count = profile.to_watch.all().count()
  review_count = Review.objects.filter(user=user).count()
  context ={'profile':profile,'watched':watched_count,'watchlist':watchlist_count,'review':review_count}
  return render(request,'profile.html',context)