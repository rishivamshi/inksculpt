from rest_framework   import generics 
from django.db.models import Q #19

from rest_framework import permissions

from sculpts.models   import Sculpt #2
from .serializers     import SculptModelSerializer #1



class SculptCreateAPIView(generics.CreateAPIView):
	serializer_class = SculptModelSerializer
	permission_classes = [permissions.IsAuthenticated]
	def perform_create(self, serializer):
		serializer.save(user = self.request.user)


class SculptListAPIView(generics.ListAPIView):
	serializer_class = SculptModelSerializer

	def get_queryset(self, *args, **kwargs): #18
		qs = Sculpt.objects.all().order_by("-timestamp") #21
		print(self.request.GET) #prints the querydict 
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


a js function in list_view.html or base.html is used to get the q or the search query. it's done in this way because we are using an api to search for the data also. function name is getParameterByName() and link - https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144
'''