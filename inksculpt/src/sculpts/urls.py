
# we have to wrap this list of urls to the main one i.e to the urls of inksculpt. insculpt/urls.py

from django.conf.urls import url
from django.urls import re_path
# from .views import sculpt_detail_view, sculpt_list_view # comments 1

from django.views.generic.base import RedirectView #9

from .views import (
    ResculptView,
	SculptCreateView,
	SculptDetailView,
	SculptListView, # 4
	SculptUpdateView,
    SculptDeleteView,
    SculptFeaturedListView
 		)
urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # url(r'^$', sculpt_list_view, name = 'list'), # 2
    # url(r'^1/$', sculpt_detail_view, name = 'detail'), # 3
    re_path(r'^$', RedirectView.as_view(url = "/"), name = 'sculpt-home'), #10
    re_path(r'^search/$', SculptListView.as_view(), name = 'list'), # 5  # /sculpt/ #8
    re_path(r'^create/$', SculptCreateView.as_view(), name = 'create'), # 7  # /sculpt/create
    re_path(r'^featured/$', SculptFeaturedListView.as_view(), name = 'featured'),
    re_path(r'^(?P<pk>\d+)/$', SculptDetailView.as_view(), name = 'detail'), # 6  # /sculpt/1
    re_path(r'^(?P<pk>\d+)/resculpt/$', ResculptView.as_view(), name = 'detail'), # 6  # /sculpt/1
    re_path(r'^(?P<pk>\d+)/update/$', SculptUpdateView.as_view(), name = 'update'), # 6  # /sculpt/1/update
    re_path(r'^(?P<pk>\d+)/delete/$', SculptDeleteView.as_view(), name = 'delete'), # 6  # /sculpt/1/delete
]






'''
Comments - 

1. importing retrieve view from views.py of sculpts app. it has two functions - sculpt_detail_view and sculpt_list_view
2. url for list view
3. url for detail view
4. importing retrieve class based views from views.py from sculpts app. 
5. .asview() turns that into an view function and its for list view
6. its for detailview.
7. url for createview. 
8. changed home to listview, and /sculpt to search view. so, /sculpt gives a page not found, which i will redirect it to home page.
9. importing redirectview to redirect /sculpt to home page.
10. this will redirect /sculpt to / which is home page.
(?P<pk>\d+) is a regular expression only for numbers.

'''