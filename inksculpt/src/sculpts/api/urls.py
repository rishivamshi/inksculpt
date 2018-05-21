
# we have to wrap this list of urls to the main one i.e to the urls of inksculpt. insculpt/urls.py

from django.conf.urls import url


from django.views.generic.base import RedirectView 

from .views import (
	LikeToggleAPIView,
	SculptCreateAPIView, #2
	SculptListAPIView, #1
	ResculptAPIView,
	SculptDetailAPIView,
	SculptFeaturedAPIView
	
 		)
urlpatterns = [

	url(r'^$', SculptListAPIView.as_view(), name = 'list'), #/api/sculpt/
  	url(r'^create/$', SculptCreateAPIView.as_view(), name='create'),
  	url(r'^(?P<pk>\d+)/resculpt/$', ResculptAPIView.as_view(), name='resculpt' ),
  	url(r'^(?P<pk>\d+)/$', SculptDetailAPIView.as_view(), name='detail' ),
  	url(r'^featured/$', SculptFeaturedAPIView.as_view(), name='featured' ),
  	url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle' )

]






'''
Comments - 

#1 - importing the view from views.py
#2 - importing the view from views.py

'''