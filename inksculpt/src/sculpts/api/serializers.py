from rest_framework import serializers #1

from django.utils.timesince import timesince #10

from accounts.api.serializers import UserDisplaySerializer #4

from sculpts.models import Sculpt #2





class ParentSculptModelSerializer(serializers.ModelSerializer): 
	user = UserDisplaySerializer(read_only=True) 
	date_display = serializers.SerializerMethodField() 
	
	timesince = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	did_like = serializers.SerializerMethodField()
	class Meta:
		model = Sculpt
		fields = [
			'id',
			'user',
			'content',
			'image',
			'timestamp',
			'date_display', 
			'timesince', 
			'likes',
			'did_like',

		]

	def get_did_like(self, obj):
		request = self.context.get("request")
		try: 			
			user = request.user
			if user.is_authenticated():
				if user in obj.liked.all():
					return True
		except:
			pass
		return False

	def get_likes(self, obj):
		return obj.liked.all().count()
	


	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d, %Y | at %I: %M %p") 

	def get_timesince(self, obj):
		return timesince(obj.timestamp) + " ago" 









class SculptModelSerializer(serializers.ModelSerializer): #3
	parent_id = serializers.CharField(write_only = True, required = False)
	user = UserDisplaySerializer(read_only=True) #5
	current_user = serializers.SerializerMethodField('_user')
	date_display = serializers.SerializerMethodField() #8
	timesince = serializers.SerializerMethodField()
	parent = ParentSculptModelSerializer( read_only = True )
	likes = serializers.SerializerMethodField()
	did_like = serializers.SerializerMethodField()

	class Meta:
		model = Sculpt
		fields = [
		'parent_id',
			'id',

			'user',
			'current_user',
			'content',
			'image',
			'timestamp',
			'date_display', #6
			'timesince', #7
			'parent',
			'likes',
			'did_like',
			'reply',
			'featured',

		]
		#read_only_fields = ['reply']

	def get_did_like(self, obj):
		request = self.context.get("request")
		try: 			
			user = request.user
			if user.is_authenticated():
				if user in obj.liked.all():
					return True
		except:
			pass
		return False

	def get_likes(self, obj):
		return obj.liked.all().count()

	def _user(self,obj):
		user = ''
		try:
			user = self.context['request'].user.username
		except:
			pass
		return user
	


	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d, %Y | at %I: %M %p") #9

	def get_timesince(self, obj):
		return timesince(obj.timestamp) + " ago" #11







'''
Comments - 

#1 - Importing serializers from rest_framework
#2 - Importing the Sculpt model from sculpts.model 
#3 - serializer is created and this serializer is used to put into the view
#4 - UserDisplaySerializer shows the user information. without this the api only shows the id of the user not the username or other details. 
#5 - Read_only is true because without this the api will also ask for the user details while creating content.

#6 - date_display gets the date at which it has sculpted.
#7 - timesince does what the name suggests.
#8 - creates a serializer method field.
#9 - from the python documentation. strftime() - formatting the time function.
#10 - import the timesince module. its inbuilt into django. 
#11 - go to the url to see how it works. /api/sculpts/
'''