"""inksculpt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include # to include the urls of apps.
from django.urls import re_path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


from accounts.views import UserRegisterView
from sculpts.views import SculptListView #1
from hashtags.api.views import TagSculptAPIView
from hashtags.views import HashTagView

from .views import home




urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', SculptListView.as_view(), name = 'home'),

    re_path(r'^tags/(?P<hashtag>.*)/$', HashTagView.as_view(), name = 'hashtag'), # url for hashtags app. 
    re_path(r'^sculpt/', include(('sculpts.urls', 'sculpt'), namespace = 'sculpt')), # url for sculpts app. 

    re_path(r'^api/tags/(?P<hashtag>.*)/$', TagSculptAPIView.as_view(), name='tag-sculpt-api'),

    re_path(r'^api/sculpt/', include(('sculpts.api.urls', 'sculpt-api'), namespace = 'sculpt-api')), #url for api
    re_path(r'^api/', include(('accounts.api.urls', 'profiles-api'), namespace = 'profiles-api')), #url for api

    
    re_path(r'^notifications/', include('notify.urls', 'notifications')),
   
    

    re_path(r'^register/$', UserRegisterView.as_view(), name='register'),

    re_path(r'^', include('allauth.urls')),
    re_path(r'^', include(('accounts.urls', 'profiles' ), namespace = 'profiles')), # url for usernames from accounts app.
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
1. SculptListView is imported to allow sculpting from the home page itself.


'''