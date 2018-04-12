from rest_framework import generics 

from sculpts.models import Sculpt #2
from .serializers import SculptModelSerializer #1

class SculptListAPIView(generics.ListAPIView):
	serializer_class = SculptModelSerializer

	def get_queryset(self):
		return Sculpt.objects.all()







'''
Comments - 

#1 - SculptModelSerializer is imported from serializers.py file.
#2 - Sculpt model has queryset which is required in SculptListAPIView.

'''