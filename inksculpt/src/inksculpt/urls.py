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
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


from accounts.views import UserRegisterView
from sculpts.views import SculptListView #1
from hashtags.api.views import TagSculptAPIView
from hashtags.views import HashTagView

from .views import home





urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SculptListView.as_view(), name = 'home'),

    url(r'^tags/(?P<hashtag>.*)/$', HashTagView.as_view(), name = 'hashtag'), # url for hashtags app. 
    url(r'^sculpt/', include('sculpts.urls', namespace = 'sculpt')), # url for sculpts app. 

    url(r'^api/tags/(?P<hashtag>.*)/$', TagSculptAPIView.as_view(), name='tag-sculpt-api'),

    url(r'^api/sculpt/', include('sculpts.api.urls', namespace = 'sculpt-api')), #url for api
    url(r'^api/', include('accounts.api.urls', namespace = 'profiles-api')), #url for api

    
   url(r'^summernote/', include('django_summernote.urls')),

    url(r'^register/$', UserRegisterView.as_view(), name='register'),

    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('accounts.urls', namespace = 'profiles')), # url for usernames from accounts app.
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
1. SculptListView is imported to allow sculpting from the home page itself.


'''