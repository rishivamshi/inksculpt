from django.db import models

from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL , related_name='profile') #1
	following 	= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True ,related_name='followed_by') #2


	def __sts__(self):
		return str(self.following.all().count()) #3

'''
Comments - 

#1 - following a user - user.profile its gonna give the profile for the user.
#2 - we can follow a lot of user and a lot of users can follow us. user.profile.following gives all the users i follow. user.followed_by gives the users that follow me(reverse).
#3 - counts the number of followers


'''