from django.contrib.auth import get_user_model #1
from rest_framework import serializers #2

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			#email

		]








'''
Comments - 

#1. getting the user model from get_user_model
#2. importing the serializer from rest_framework
#3. Its the serializer to publically display the user details. the api in itself shows the id of the user instead of the name. but with this, it will show the name of the user.


'''