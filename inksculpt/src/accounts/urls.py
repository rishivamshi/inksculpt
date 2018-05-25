
# we have to wrap this list of urls to the main one i.e to the urls of inksculpt. insculpt/urls.py

from django.conf.urls import url, include
# from .views import sculpt_detail_view, sculpt_list_view # comments 1

from django.views.generic.base import RedirectView #9

from .views import (
	UserDetailView, #4
	UserFollowView, #10
	UserAlbumListView
 		)
urlpatterns = [
	

    url(r'^(?P<username>[\w.@+-]+)/album/$', UserAlbumListView.as_view(), name = 'album'),

    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name = 'detail'), # 6  # /sculpt/1
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name = 'follow'), # 6  # /sculpt/1
   
]






'''
Comments - 

1. importing retrieve view from views.py of sculpts app. it has two functions - sculpt_detail_view and sculpt_list_view

4. Importing UserDetailView from views.py 
10. importing the toggle_follow class from views.py


8. changed home to listview, and /sculpt to search view. so, /sculpt gives a page not found, which i will redirect it to home page.
9. importing redirectview to redirect /sculpt to home page.

(?P<pk>\d+) is a regular expression only for numbers.

'''