from rest_framework import serializers #1

from accounts.api.serializers import UserDisplaySerializer #4

from sculpts.models import Sculpt #2

class SculptModelSerializer(serializers.ModelSerializer): #3
	user = UserDisplaySerializer()
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
#4 - UserDisplaySerializer shows the user information. without this the api only shows the id of the user not the username or other details. 


'''