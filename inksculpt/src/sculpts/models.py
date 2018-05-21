import re
from django.db.models.signals import post_save

from django.conf import settings # comments -2 
from django.urls import reverse #3
from django.core.exceptions import ValidationError # for validation
from django.db import models


from django.db.models import TextField 
from django.utils import timezone

from hashtags.signals import parsed_hashtags


class NonStrippingTextField(TextField):
	def formfield(self, **kwargs):
		kwargs['strip'] = False 
		return super(NonStrippingTextField,self).formfield(**kwargs)


def upload_location(object, filename): #5
	return "%s/%s" %(object.user, filename)

# for validation

from .validators import validate_content





# Create your models here.
class SculptManager(models.Manager):
	def resculpt(self, user, parent_obj):

		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj

		qs = self.get_queryset().filter(
			user = user,
			parent = og_parent).filter(
				timestamp__year = timezone.now().year,
				timestamp__month = timezone.now().month,
				timestamp__day = timezone.now().day,
				reply = False,
				)
		if qs.exists():
			return None 


		obj = self.model(
			parent = og_parent,
			user = user, 
			content = parent_obj.content,
			image = parent_obj.image,
			)
		obj.save()
		return obj

	def like_toggle(self, user, sculpt_obj):
		if user in sculpt_obj.liked.all():
			is_liked = False 
			sculpt_obj.liked.remove(user)

		else:
			is_liked =  True
			sculpt_obj.liked.add(user)

		return is_liked




class Sculpt(models.Model):
	parent = models.ForeignKey("self", blank = True, null = True)
	user = models.ForeignKey( settings.AUTH_USER_MODEL ) # Comments - 1 and attribute is cooments 2. 
	content = NonStrippingTextField(validators = [validate_content]) # writing stuff and see how to take care of blank spaces - strip = false
	liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = 'liked')
	reply = models.BooleanField(verbose_name = 'Is a reply?', default = False)
	featured = models.BooleanField(verbose_name='Featured aah? haha', default = False)
	image = models.ImageField(
				upload_to = upload_location,
				null = True,
				blank = True,
				width_field = "width_field",
				height_field = "height_field") # images stuff
		
	height_field = models.IntegerField(default = 0) #4
	width_field = models.IntegerField(default = 0)
	updated = models.DateTimeField(auto_now = True) # if the content is updated
	timestamp = models.DateTimeField( auto_now_add = True ) # autonowadd means it will automatically create it fo us, when we create content. 

	objects = SculptManager()

	# this function is to change the name from sculptobject to actual written sculpt in admin page.
	def __str__(self):
		return str(self.content) #self.id can also be added here.

	def get_absolute_url(self):
		return reverse("sculpt:detail", kwargs={"pk":self.pk}) # if theirs no success_url in the views class, it will go this url

	# the following class allows to print the sculpts in reverse order(timestamp). migrations to run this thing. but I am not doing it here, as i am doing it in the api/views.py.
	class Meta:
		ordering = ['-timestamp']

	def get_parent(self):
		the_parent = self
		if self.parent:
			the_parent = self.parent
		return the_parent

	def get_children(self):
		parent = self.get_parent()
		qs = Sculpt.objects.filter(parent=parent)
		qs_parent = Sculpt.objects.filter(pk = parent.pk)
		return (qs | qs_parent) 

	# validation can be done in the models itself. 
	# this will be called , whenever you even want to save the model itself.
	# def clean(self, *args, **kwargs ):
	# 	content = self.content
	# 	if content == "abc":
	# 		raise ValidationError("Cannot be ABC")
	# 	return super(Sculpt, self).clean(*args, **kwargs)


def sculpt_save_receiver(sender, instance, created, *args, **kwargs):

	if created and not instance.parent:
		#notify a user.
		user_regex = r'@(?P<username>[\w.@+-]+)'
		usernames = re.findall(user_regex, instance.content)
		# send notification to user here.

		hash_regex = r'#(?P<hashtag>[\w\d-]+)'
		hashtags = re.findall(hash_regex, instance.content)
		parsed_hashtags.send(sender = instance.__class__, hashtag_list = hashtags)
		#send hashtag signal to user here
		

post_save.connect(sculpt_save_receiver, sender = Sculpt)
'''
COMMENTS - All reasons 


1. foreign key connects different models together. creates a relationship between two models. We have to use foreignkey to associate sculpts with users. 
2. to associate with the user model we bring actual path to the user model. 
3. 24.
4. ImageField Documentation. It has two attributes, height_field and width_field, which can be used to know about the res of the image. 
5. it creates a more dynamic upload location. it saves inside the user/image. 


'''

