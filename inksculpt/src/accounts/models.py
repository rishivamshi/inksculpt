from django.db import models

from django.conf import settings

from django.urls import reverse_lazy

from django.db.models.signals import post_save #12
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from django_countries.fields import CountryField

def upload_location(object, filename): #5
	return "%s/%s/%s" %(object.user,"displaypicture", filename)


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

	def toggle_follow(self, user, to_toggle_user):
		user_profile, created = UserProfile.objects.get_or_create(user=user) # creates a tuple (user_obj, true) 
		if to_toggle_user in user_profile.following.all(): #11
			user_profile.following.remove(to_toggle_user)
			added = False
		else:
			user_profile.following.add(to_toggle_user)
			added = True
		return added

	def is_following(self, user, followed_by_user):
		user_profile, created = UserProfile.objects.get_or_create(user = user)

		if created:
			return False
		if followed_by_user in user.profile.following.all():
			return True
		return False


	def recommended(self, user, limit_to = 10):
		profile = user.profile 
		following = profile.get_following()
		qs = self.get_queryset().exclude(user__in = following).exclude(id = profile.id).order_by("?")[:limit_to]
		return qs




class UserProfile(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL , related_name='profile', null = True, on_delete = models.SET_NULL) #1
	following 	= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True ,related_name='followed_by') #2

	profile_image = models.ImageField(
				upload_to = upload_location,
				null = True,
				blank = True,
				width_field = "width_profilefield",
				height_field = "height_profilefield") # images stuff
		
	height_profilefield = models.IntegerField(default = 0, null = True, blank = True) 
	width_profilefield = models.IntegerField(default = 0, null = True, blank = True)


	cover_image = models.ImageField(
				upload_to = upload_location,
				null = True,
				blank = True,
				width_field = "width_coverfield",
				height_field = "height_coverfield") # images stuff
		
	height_coverfield = models.IntegerField(default = 0, null = True, blank = True) 
	width_coverfield = models.IntegerField(default = 0, null = True, blank = True)




	dob = models.DateField(null = True, blank = True)

	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('U', 'Unspecified'),
		)



	

	gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, null = True)
	city	= models.CharField(max_length = 140, null = True, blank = True)
	country = CountryField(blank = True, null = True)
	status = models.CharField(max_length = 140, null = True, blank = True)
	phone_number = models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$'),MinLengthValidator(10)], null = True, blank = True)





	objects  = UserProfileManager() # UserProfile.objects.all() #5

	def __str__(self):	
		return str(self.user)


	def __sts__(self):
		return str(self.following.all().count()) #3

	def get_profileurl(self):
		return profile_image

	def get_following(self): #8
		users = self.following.all() # User.objects.all().exclude(username = self.user.username)
		return users.exclude(username = self.user.username)

	def get_follow_url(self):
		return reverse_lazy("profiles:follow", kwargs= {"username": self.user.username})

	def get_absolute_url(self):
		return reverse_lazy("profiles:detail", kwargs= {"username": self.user.username})




''' 
explaining the following signal code 

rishi = User.objects.first()
User.objects.get_or_create() #(user_obj, true/false)
cfe.save()

'''

def post_save_user_receiver(sender, instance, created, *args, **kwargs): #13
	# print(instance)
	if created:
		new_profile  = UserProfile.objects.get_or_create(user=instance)
		

		# using celery + redis , we can do some deferred task.



post_save.connect(post_save_user_receiver, sender = settings.AUTH_USER_MODEL)



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

#11 - if user is already following, then unfollow, if not then follow.

#12 - this helps create user profile once the user signsup, so that other users can follow him. it uses post_save signal, that when pressed will create user profile.

#13 - post save signal for the user. docs.djangoproject.com/en/1.10/ref/signals/#post-save

'''