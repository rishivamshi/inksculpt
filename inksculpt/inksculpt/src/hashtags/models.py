from django.db import models
from django.urls import reverse_lazy


from sculpts.models import Sculpt #3

from .signals import parsed_hashtags

# Create your models here.
class HashTag(models.Model):
	tag = models.CharField(max_length = 120) #1 
	timestamp = models.DateTimeField(auto_now_add = True) #2

	def __str__(self): #__unicode__
		return self.tag

	def get_absolute_url(self):
		return reverse_lazy("hashtag", kwargs= {"hashtag": self.tag})


	def get_sculpts(self):
		return Sculpt.objects.filter(content__icontains = "#" + self.tag)


def parsed_hashtags_receiver(sender , hashtag_list, *args, **kwargs):
	if len(hashtag_list) > 0:
		for tag_var in hashtag_list:
			new_tag, create = HashTag.objects.get_or_create(tag = tag_var)


parsed_hashtags.connect(parsed_hashtags_receiver)
'''
Comments - 

#1 - maxlength is for the max length of the hashtag
#2 - DateTimeField will give the time at which the hashtag is created
#3 - this is added to get the hashtags created in sculpt model. the get_sculpts function filters the content for # and adds it to the tag.


'''