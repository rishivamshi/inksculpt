from django.contrib.auth import get_user_model #1

from django.urls import reverse_lazy


from rest_framework import serializers #2

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
	follower_count = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	dp_url = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'follower_count',
			'url',
			'dp_url',
			#email

		]

	def get_follower_count(self, obj):
		return 0

	def get_url(self, obj):
		return reverse_lazy("profiles:detail", kwargs = {"username": obj.username })
	
	def get_dp_url(self, obj):

		return obj.profile.profile_image.url
	







'''
Comments - 

#1. getting the user model from get_user_model
#2. importing the serializer from rest_framework
#3. Its the serializer to publically display the user details. the api in itself shows the id of the user instead of the name. but with this, it will show the name of the user.


'''