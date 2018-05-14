from rest_framework   import generics 
from django.db.models import Q #19

from rest_framework import permissions #22

from sculpts.models   import Sculpt #2

from .pagination 	import StandardResultsPagination #24
from .serializers     import SculptModelSerializer #1


from rest_framework.views import APIView 
from rest_framework.response import Response 


class LikeToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,pk, format = None):
		sculpt_qs = Sculpt.objects.filter(pk = pk)
		message = "Not allowed"
		
		if request.user.is_authenticated():
			is_liked = Sculpt.objects.like_toggle(request.user, sculpt_qs.first())
			return Response({'liked': is_liked })
		
		return Response({"message": message }, status = 400)




class ResculptAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,pk, format = None):
		sculpt_qs = Sculpt.objects.filter(pk = pk)
		message = "Not allowed"
		if sculpt_qs.exists() and sculpt_qs.count() == 1:
			
			new_sculpt = Sculpt.objects.resculpt(request.user, sculpt_qs.first())
			if new_sculpt is not None:
				data = SculptModelSerializer(new_sculpt).data	
				return Response(data)
			message = "Cannot resculpt the same in one day"
		return Response({"message": message }, status = 400)



class SculptCreateAPIView(generics.CreateAPIView):
	serializer_class = SculptModelSerializer
	permission_classes = [permissions.IsAuthenticated] #23
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)


class SculptDetailAPIView(generics.ListAPIView):
	queryset = Sculpt.objects.all()
	serializer_class = SculptModelSerializer
	pagination_class = StandardResultsPagination
	permission_classes = [permissions.AllowAny] 
	
	def get_queryset(self, *args, **kwargs):
		sculpt_id = self.kwargs.get("pk")
		# print(sculpt_id)
		qs = Sculpt.objects.filter(pk = sculpt_id)
		if qs.exists() and qs.count() == 1:
			parent_obj = qs.first()
			qs1 = parent_obj.get_children()
			qs = (qs | qs1).distinct().extra(select = {"parent_id_null": 'parent_id IS NULL'})

		return qs.order_by("-parent_id_null", '-timestamp')


class SculptListAPIView(generics.ListAPIView):
	serializer_class = SculptModelSerializer
	pagination_class = StandardResultsPagination
	permission_classes = [permissions.AllowAny]
	queryset = Sculpt.objects.all()

	def get_serializer_context(self, *args, **kwargs):
		context = super(SculptListAPIView, self ).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs): #18
		requested_user = self.kwargs.get("username")
		if requested_user:


			qs = Sculpt.objects.filter(user__username = requested_user).order_by("-timestamp")

		else:
			# qs = Sculpt.objects.filter(user__in = im_following).order_by("-timestamp") #21
			im_following = self.request.user.profile.get_following()
			qs1 = Sculpt.objects.filter(user__in = im_following)
			qs2 = Sculpt.objects.filter(user = self.request.user)

			qs = (qs1 | qs2).distinct().order_by("-timestamp")

			# print(self.request.GET) #prints the querydict 
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter (

				Q(content__icontains = query) | 
				Q(user__username__icontains = query)
				
				)

		return qs #20


'''
Comments - 

#1  - SculptModelSerializer is imported from serializers.py file.
#2  - Sculpt model has queryset which is required in SculptListAPIView.
#18 - this function generates a query dictionary.if we print(self.qs.GET) it prints a querydict. if the url is updats to 12.../sculpt/?q=some search, it prints this q in the qwerydict which allows to search.
#19 - This import allows us to search for more fields. its a complex lookup. https://docs.djangoproject.com/en/1.10/topics/db/queries/
#20 - this entire functions just makes list view more robust as it allows for searching sculpts. from search_view.html, search term is extracted and then that term is passed in this function to search if the terms is in the database and then if present, it users list_view.html to show them.


#21 - it can be replaced with -pk = primary key as it increases by 1.


#23 - checks if the create url is user authenticated or not. basically, you cannot post stuff if user is not signed up.
#24 - importing the pagination class from pagination.py


a js function in list_view.html or base.html is used to get the q or the search query. it's done in this way because we are using an api to search for the data also. function name is getParameterByName() and link - https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144
'''