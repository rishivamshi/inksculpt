from django.db import models

from django.conf import settings

# Create your models here.

class UserProfileManager(models.Manager): #4
	def all(self):
		qs = self.get_queryset().all()
		# print(dir(self)) #6 
		# print(self.instance) #user
		try:
			if self.instance:
				qs = qs.exclude(user = self.instance) #7
		except:
			pass
		return qs



class UserProfile(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL , related_name='profile') #1
	following 	= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True ,related_name='followed_by') #2


	objects  = UserProfileManager() # UserProfile.objects.all() #5

	def __sts__(self):
		return str(self.following.all().count()) #3

	def get_following(self): #8
		users = self.following.all() # User.objects.all().exclude(username = self.user.username)
		return users.exclude(username = self.user.username)

'''
Comments - 

#1 - following a user - user.profile its gonna give the profile for the user.
#2 - we can follow a lot of user and a lot of users can follow us. user.profile.following gives all the users i follow. user.followed_by gives the users that follow me(reverse).
#3 - counts the number of followers
#4 - this class is used to override .all so that the user will not follow himself.
#5 - it creates a model manager. 
#6 - prints all the available methods inside of self.
#7 - removes the user from the qs so that it will not show the user following himself because of reverse relationship.
#8 - this to remove me from the followers 
'''