
# we have to wrap this list of urls to the main one i.e to the urls of inksculpt. insculpt/urls.py

from django.conf.urls import url


from django.views.generic.base import RedirectView 

from .views import (
	SculptListAPIView, #1
	
 		)
urlpatterns = [

	url(r'^$', SculptListAPIView.as_view(), name = 'list'), #/api/sculpt/
   
]






'''
Comments - 

#1 - importing the view from views.py


'''