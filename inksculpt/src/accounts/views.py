from django.contrib.auth import get_user_model #3
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.shortcuts import render
from django.shortcuts import get_object_or_404 #4
from django.shortcuts import redirect #6
from django.views import View #5
from django.views.generic import DetailView, ListView #1
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from .forms import UserRegisterForm
from .models import UserProfile #9
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import UserForm, ProfileForm, ProfileImageForm
from sculpts.mixins import UserOwnerMixin

User = get_user_model()




def update_profile(request):
	# instance = get_object_or_404(User, username__iexact = self.kwargs.get('username'))

	if request.method == 'POST':
		user_form = UserForm(request.POST, instance = request.user)
		profile_form = ProfileForm(request.POST, instance = request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			# messages.success(request, _('Your profile was successfully updated!'))
			return redirect('/')

		# else:
			# messages.error(request, _('Please correct the error below.'))

	else:
		user_form = UserForm(instance = request.user)
		profile_form = ProfileForm(instance = request.user.profile)

	return render(request, 'accounts/user_profile.html', {
		'user_form': user_form,
		'profile_form': profile_form,
		})


def update_imageprofile(request):
	# instance = get_object_or_404(User, username__iexact = self.kwargs.get('username'))

	if request.method == 'POST':
		
		profileimage_form = ProfileImageForm(request.POST,request.FILES, instance = request.user.profile)
		if profileimage_form.is_valid():
			
			profileimage_form.save()
			# messages.success(request, _('Your profile was successfully updated!'))
			return redirect('/')

		# else:
			# messages.error(request, _('Please correct the error below.'))

	else:
		
		profileimage_form = ProfileImageForm(instance = request.user.profile)

	return render(request, 'accounts/user_profileimage.html', {
		
		'profileimage_form': profileimage_form,
		})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


	


# Create your views here.

class UserRegisterView(FormView):
	template_name = 'registration/user_register_form.html'
	form_class = UserRegisterForm
	success_url = '/login'

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		first_name = form.cleaned_data.get("first_name")
		last_name = form.cleaned_data.get("last_name")
		new_user = User.objects.create(username = username, email = email, first_name = first_name, last_name  = last_name)
		new_user.set_password(password)

		new_user.save()
		return super(UserRegisterView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		data = super (UserRegisterView, self).get_context_data(**kwargs)
		data['my_reg_form'] = data.get('form')
		return data
	



class UserDetailView(DetailView):	#2
	template_name = 'accounts/user_detail.html'
	queryset = User.objects.all()

	def get_object(self):
		return get_object_or_404(User, username__iexact = self.kwargs.get("username"))


	def get_context_data(self, *args, **kwargs):
		context = super(UserDetailView, self).get_context_data(*args, **kwargs)
		following = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['recommended'] = UserProfile.objects.recommended(self.request.user)

		return context

class UserFollowView(View): #7
	def get(self, request, username, *args, **kwargs):

		toggle_user = get_object_or_404(User, username__iexact = username) #to get the user #8
		if request.user.is_authenticated():
			is_following = UserProfile.objects.toggle_follow(request.user , toggle_user)
		return redirect("profiles:detail", username = username)




class UserAlbumListView(DetailView): #7
	template_name = 'accounts/user_album.html'
	queryset = User.objects.all()

	def get_object(self):
		return get_object_or_404(User, username__iexact = self.kwargs.get("username"))


	def get_context_data(self, *args, **kwargs):
		context = super(UserAlbumListView, self).get_context_data(*args, **kwargs)
		following = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['recommended'] = UserProfile.objects.recommended(self.request.user)

		return context


class UserFollowingListView(DetailView): #7
	template_name = 'accounts/user_following.html'
	queryset = User.objects.all()

	def get_object(self):
		return get_object_or_404(User, username__iexact = self.kwargs.get("username"))


	def get_context_data(self, *args, **kwargs):
		context = super(UserFollowingListView, self).get_context_data(*args, **kwargs)
		following = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['recommended'] = UserProfile.objects.recommended(self.request.user)

		return context


class UserFollowersListView(DetailView): #7
	template_name = 'accounts/user_followers.html'
	queryset = User.objects.all()

	def get_object(self):
		return get_object_or_404(User, username__iexact = self.kwargs.get("username"))


	def get_context_data(self, *args, **kwargs):
		context = super(UserFollowersListView, self).get_context_data(*args, **kwargs)
		following = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['recommended'] = UserProfile.objects.recommended(self.request.user)

		return context


class UserAboutView(DetailView): #7
	template_name = 'accounts/user_about.html'
	queryset = User.objects.all()
	

	def get_object(self):
		return get_object_or_404(User, username__iexact = self.kwargs.get("username"))


	def get_context_data(self, *args, **kwargs):
		context = super(UserAboutView, self).get_context_data(*args, **kwargs)
		following = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['recommended'] = UserProfile.objects.recommended(self.request.user)

		return context

	
	

'''
Comments - 

#1 - importing the detail view from django.views
#2 - DetailView is from #1
#3 - getting the user model in django.contrib.auth
#4 - this is imported to change the user url from /pk to /username using slug field. connected to #5
#5 - importing class based view.
#6 - redirect is imported because when user clicks on follow button, it redirects to itself 
#7 - to toggle follow 
#8 - its showing error because request.user.profile might not actually exist. so that's why i am importing UserProfile from .models #9 and changing it to the current version.






'''