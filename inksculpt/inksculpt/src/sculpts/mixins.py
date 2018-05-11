from django import forms
from django.forms.utils import ErrorList # to do some stuff if form is invalid.

class FormUserNeededMixin(object):
	def form_valid(self, form):
		# this method is called when valid form data has been POSTed.
		# it should return an HttpResponse.

		# form.instance.user = self.request.user
		# return super(SculptCreateView, self).form_valid(form)
		# 12

		if self.request.user.is_authenticated():
			form.instance.user = self.request.user
			return super(FormUserNeededMixin, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
			return self.form_invalid(form)


# UserOwnerMixin is to makesure that only that user can update the content. which avoids other users to update other users content. i know, it sounds silly.

class UserOwnerMixin(FormUserNeededMixin, object):
	def form_valid(self, form):
		if form.instance.user == self.request.user: # to check if both the users are same.
			return super(UserOwnerMixin, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["This user is not allowed to change this data"])
			return self.form_invalid(form)
