


from django.conf.urls import url


from django.views.generic.base import RedirectView 

from sculpts.api.views import (
	
	SculptListAPIView, 
	
 		)
urlpatterns = [

	url(r'^(?P<username>[\w.@+=]+)/sculpt/$', SculptListAPIView.as_view(), name = 'list'), 
  	
]





