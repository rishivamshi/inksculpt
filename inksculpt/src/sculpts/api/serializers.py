from rest_framework import serializers #1

from sculpts.models import Sculpt #2

class SculptModelSerializer(serializers.ModelSerializer): #3
	class Meta:
		model = Sculpt
		fields = [
			'user',
			'content',
			'image'

		]









'''
Comments - 

#1 - Importing serializers from rest_framework
#2 - Importing the Sculpt model from sculpts.model 
#3 - serializer is created and this serializer is used to put into the view



'''