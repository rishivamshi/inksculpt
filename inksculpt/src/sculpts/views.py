from django.contrib.auth.mixins import LoginRequiredMixin #14
from django.db.models import Q #19
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse #17
from django.views.generic import DetailView, ListView #5
from django.views.generic import CreateView #10
from django.views.generic import UpdateView #15
from django.views.generic import DeleteView #16
from .forms import SculptModelForm # 11
from .mixins import FormUserNeededMixin # importing from mixins.py to validate if user is logged in or not.
from .mixins import UserOwnerMixin # see mixins.py
from .models import Sculpt #1

from django.views import View
from django.http import HttpResponseRedirect
from accounts.models import UserProfile

# Create your views here.

class ResculptView(View):
	def get(self, request, pk, *args, **kwargs):
		sculpt = get_object_or_404(Sculpt, pk=pk)
		if request.user.is_authenticated:
			new_sculpt = Sculpt.objects.resculpt(request.user, sculpt)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(sculpt.get_absolute_url())

# create 
# Create view is similar to the admin form. 
class SculptCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = SculptModelForm 
	template_name = 'sculpts/create_view.html'
	#success_url = reverse_lazy('sculpt:detail')
	login_url = '/admin/'
	# and take this createview and add it into urls.

	# 13
	# def form_valid(self, form):
	# 	# this method is called when valid form data has been POSTed.
	# 	# it should return an HttpResponse.

	# 	# form.instance.user = self.request.user
	# 	# return super(SculptCreateView, self).form_valid(form)
	# 	# 12

	# 	if self.request.user.is_authenticated:
	# 		form.instance.user = self.request.user
	# 		return super(SculptCreateView, self).form_valid(form)
	# 	else:
	# 		form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
	# 		return self.form_invalid(form)



# update
class SculptUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Sculpt.objects.all()
	form_class = SculptModelForm
	template_name = 'sculpts/update_view.html'
	#success_url = '/sculpt/'
	# login_url = '/admin/' #it has a default url, which i will update during user signup




#delete
class SculptDeleteView(LoginRequiredMixin, DeleteView):
	model = Sculpt
	template_name = 'sculpts/delete_confirm.html' # delete view template
	success_url = reverse_lazy("sculpt:list") #/sculpt/list
	def get_queryset(self):
		qs = super(SculptDeleteView, self).get_queryset()
		return qs.filter(user = self.request.user)


#retrieve

class SculptDetailView(DetailView): #6
	template_name = "sculpts/detail_view.html" #8
	queryset = Sculpt.objects.all()

	# def get_object(self):
	# 	# print(self.kwargs) #9
	# 	pk = self.kwargs.get("pk")
	#   obj = get_object_or_404(Sculpt, pk = pk)
	# 	return Sculpt.objects.get(id =pk )

class SculptListView(LoginRequiredMixin, ListView): #7
	template_name = "sculpts/list_view.html"
	#queryset = Sculpt.objects.all() 

	def get_queryset(self, *args, **kwargs): #18
		qs = Sculpt.objects.all()
		#print(self.request.GET) #prints the querydict 
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter (
				Q(content__icontains = query) | 
				Q(user__username__icontains = query)
				)

		return qs #20

	# to get context of the data.
	def get_context_data(self, *args, **kwargs):
		context = super(SculptListView, self).get_context_data(*args, **kwargs)
		context['create_form'] = SculptModelForm() #21
		context['create_url'] = reverse_lazy("sculpt:create")
		#context["another_list"] = Sculpt.objects.all()
		context['credits'] = UserProfile.objects.credits(self.request.user)
		return context


class SculptFeaturedListView(LoginRequiredMixin, ListView): #7
	template_name = "sculpts/featured.html"
	queryset = Sculpt.objects.all() 












#function based view for detail view. its the same as class - SculptDetailView
# def sculpt_detail_view(request, id = 1):

# 	obj = Sculpt.objects.get(id = id ) # 2
# 	# print(obj)


# 	context = {
# 		"object": obj
# 	}

# 	return render(request, "sculpts/detail_view.html", context) # 4
	# this is gonna get a detail of a particular sculpt.

# function based view for list view. its the same as class - SculptListView
# def sculpt_list_view(request):
# 	queryset = Sculpt.objects.all() # 3
# 	#print(queryset)
# 	#for obj in queryset:
# 	#	print(obj.content)

# 	context = {
# 		"object_list": queryset

# 	}

# 	return render(request, "sculpts/list_view.html", context)















'''
Comments 

1. importing sculpt model from models.py to query from the database. 
2. its only going to retrieve query of that id. sculpts.objects.get pulls based on id.
3. its going to retrieve query of everything in sculpt database. 
4. take the request, combine the context with the html and give the output.
5. Using classbased views to get the data from the database and query them. instead of function based views.
6. This class is used to get detail view. 
7. this class is used to get list view. queries all the data from the database. 
8. by default, these classes have their own name called template_name. so we can map it to any url.
9. everytime it runs, it searches for that url. meaning, if i change the url to something like, /sculpt/23 it searches for pk number 23. pk is in urls.py regex.
10. importing create view to get the createview class. 
11. getting the model form admin from forms.py for createview. as createview is similar to admin form.
12. the above two lines are correct only when user is logged in. if the user is not logged in, it will just simple show an error as it tries to assign anonymous user to submit the form. so, i am using if else to change that. 
13. That function can be replaced with formUserNeededMixin from mixins.py. its the same function but this method makes it a lot cleaner.
14. LoginRequiredMixin is imported to redirect to the login page if the user is not logged in. it requires a login_url in view. if i dont use this, it shows that user is needed to login i.e from formUserNeededMixin but if I use this, it overrides that custom mixin to directly reload to login url
15. Importing Update View to update content for the users.
16. Importing Delete View to allow users to delete sculpts. its directly from the documenatation of delete view.
17. (24) It allows us to have more dynamic call for any url. we can use namespace in urls.py from inksculpt(main) to map it to the app name (ex - sculpts app) and then use it to sculpt:list to map the url. 
18. this function generates a query dictionary.if we print(self.qs.GET) it prints a querydict. if the url is updats to 12.../sculpt/?q=some search, it prints this q in the qwerydict which allows to search.
19. This import allows us to search for more fields. its a complex lookup. https://docs.djangoproject.com/en/1.10/topics/db/queries/
20. this entire functions just makes list view more robust as it allows for searching sculpts. from search_view.html, search term is extracted and then that term is passed in this function to search if the terms is in the database and then if present, it users list_view.html to show them.
21. This two lines allows to sculpt from the homepage itself. as these two are linked with list_view.html with form=create_form action_url=create_url.


'''