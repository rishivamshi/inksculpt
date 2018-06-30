from django.shortcuts import render

from django.views import View


from .models import HashTag
from accounts.models import UserProfile
# Create your views here.

class HashTagView(View):
	def get(self, request, hashtag, *args, **kwargs):
		obj, created = HashTag.objects.get_or_create(tag = hashtag)
		return render(request, 'hashtags/tag_view.html', {"obj": obj})

	def get_context_data(self, *args, **kwargs):
		context = super(HashTagView, self).get_context_data(*args, **kwargs)
		
		context['credits'] = UserProfile.objects.credits(self.request.user)
		return context