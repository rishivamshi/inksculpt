
# we have to wrap this list of urls to the main one i.e to the urls of inksculpt. insculpt/urls.py

from django.conf.urls import url


from django.views.generic.base import RedirectView 

from .views import (
	SculptCreateAPIView, #2
	SculptListAPIView, #1
	
 		)
urlpatterns = [

	url(r'^$', SculptListAPIView.as_view(), name = 'list'), #/api/sculpt/
  	url(r'^create/$', SculptCreateAPIView.as_view(), name='create'),
]






'''
Comments - 

#1 - importing the view from views.py
#2 - importing the view from views.py

'''