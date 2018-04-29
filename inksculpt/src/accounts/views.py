from django.contrib.auth import get_user_model #3


from django.shortcuts import render
from django.shortcuts import get_object_or_404 #4
from django.views.generic import DetailView #1

User = get_user_model()

# Create your views here.


class UserDetailView(DetailView):	#2
	template_name = 'accounts/user_detail.html'
	queryset = User.objects.all()

	def get_object(self):
		return get_object_or_404(User, username__iexact = self.kwargs.get("username"))







'''
Comments - 

#1 - importing the detail view from django.views
#2 - DetailView is from #1
#3 - getting the user model in django.contrib.auth
#4 - this is imported to change the user url from /pk to /username using slug field. connected to #5









'''