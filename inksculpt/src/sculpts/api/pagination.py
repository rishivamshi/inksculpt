
from rest_framework import pagination #1

class StandardResultsPagination(pagination.PageNumberPagination): #2
	page_size = 10 #3
	page_size_query_param = 'page_size'
	max_page_size = 1000


class StandardResultsFeaturedPagination(pagination.PageNumberPagination): #2
	page_size = 60 #3
	page_size_query_param = 'page_size'
	max_page_size = 1000




'''
Comments -
all this pagination is from the official documentation example.

import this pagination class into the views.py

#1 - importing pagination from django rest framework. 
#2 - from the documentation - django-rest-framework.org/api-guide/pagination/
#3 - default page size.


'''