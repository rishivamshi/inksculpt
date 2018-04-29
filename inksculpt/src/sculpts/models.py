from django.conf import settings # comments -2 
from django.urls import reverse #3
from django.core.exceptions import ValidationError # for validation
from django.db import models


from django.db.models import TextField 

class NonStrippingTextField(TextField):
	def formfield(self, **kwargs):
		kwargs['strip'] = False 
		return super(NonStrippingTextField,self).formfield(**kwargs)


def upload_location(object, filename): #5
	return "%s/%s" %(object.user, filename)

# for validation

from .validators import validate_content





# Create your models here.



class Sculpt(models.Model):
	user = models.ForeignKey( settings.AUTH_USER_MODEL ) # Comments - 1 and attribute is cooments 2. 
	content = NonStrippingTextField(validators = [validate_content]) # writing stuff and see how to take care of blank spaces - strip = false
	
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


	# this function is to change the name from sculptobject to actual written sculpt in admin page.
	def __str__(self):
		return str(self.content) #self.id can also be added here.

	def get_absolute_url(self):
		return reverse("sculpt:detail", kwargs={"pk":self.pk}) # if theirs no success_url in the views class, it will go this url

	# the following class allows to print the sculpts in reverse order(timestamp). migrations to run this thing. but I am not doing it here, as i am doing it in the api/views.py.
	class Meta:
		ordering = ['-timestamp']

	# validation can be done in the models itself. 
	# this will be called , whenever you even want to save the model itself.
	# def clean(self, *args, **kwargs ):
	# 	content = self.content
	# 	if content == "abc":
	# 		raise ValidationError("Cannot be ABC")
	# 	return super(Sculpt, self).clean(*args, **kwargs)





'''
COMMENTS - All reasons 


1. foreign key connects different models together. creates a relationship between two models. We have to use foreignkey to associate sculpts with users. 
2. to associate with the user model we bring actual path to the user model. 
3. 24.
4. ImageField Documentation. It has two attributes, height_field and width_field, which can be used to know about the res of the image. 
5. it creates a more dynamic upload location. it saves inside the user/image. 


'''

