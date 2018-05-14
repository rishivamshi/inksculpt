from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response 

from sculpts.models import Sculpt 

from sculpts.api.pagination import StandardResultsPagination
from sculpts.api.serializers import SculptModelSerializer


from hashtags.models import HashTag

class TagSculptAPIView(generics.ListAPIView):
	queryset = Sculpt.objects.all().order_by("-timestamp")
	serializer_class = SculptModelSerializer
	pagination_class = StandardResultsPagination

	def get_serializer_context (self, *args, **kwargs):
		context = super(TagSculptAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request

		return context

	def get_queryset (self, *args, **kwargs):
		hashtag = self.kwargs.get("hashtag")
		hashtag_obj = None
		try: 
			hashtag_obj = HashTag.objects.get_or_create(tag = hashtag)[0]
		except:
			pass

		if hashtag_obj:
			qs = hashtag_obj.get_sculpts()

		
			query = self.request.GET.get("q", None)
			if query is not None:
				qs = qs.filter(

					Q(content__icontains = query) | 
					Q(user__username__icontains = query)

					)
			return qs
		return None