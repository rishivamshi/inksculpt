from django.contrib.auth import get_user_model #3
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.shortcuts import get_object_or_404 #4
from django.shortcuts import redirect #6
from django.views import View #5
from django.views.generic import DetailView, ListView #1

from django.views.generic.edit import FormView
from .forms import UserRegisterForm
from .models import UserProfile #9

from django.contrib.auth.mixins import LoginRequiredMixin



User = get_user_model()

# Create your views here.

class UserRegisterView(FormView):
	template_name = 'accounts/user_register_form.html'
	form_class = UserRegisterForm
	success_url = '/login'

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create(username = username, email = email)
		new_user.set_password(password)
		new_user.save()
		return super(UserRegisterView, self).form_valid(form)





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