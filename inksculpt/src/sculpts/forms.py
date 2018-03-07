# for create and update view we need forms. get the idea from admin panel. 
# views can use these forms to create and update. 
# this can be used for validation also. 
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout , Field 
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)


from .models import Sculpt

class SculptModelForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(
	 					attrs={
	 					 "class": "form-control"}))

	# image = forms.ImageField(label = '',  widget=forms.FileInput(
	# 					attrs={"class": "form-control"}))
	
	class Meta:
		model = Sculpt
		fields = [
			#"user", #1
			"content",
			"image",

		]
		# exclude = ['user'] # to exclude.

	# def __init__(self, *args, **kwargs):
	# 	super (SculptModelForm, self).__init__(*args, **kwargs)
	# 	self.helper = FormHelper()
	# 	self.helper.form_method = 'POST'
	# 	self.helper.layout = Layout(
	# 			PrependedText('content', 'Write Anything'),
				
	# 			PrependedAppendedText('image', 'Upload','Browse'),
	# 			FormActions(Submit('Sculptss', 'Sculptss', css_clss = 'btn btn-primary'))


	# 		)

	# all from official documentation 	
	# def clean_content(self, *args, **kwargs):
	# 	content = self.cleaned_data.get("content")
	# 	if content == "abc":
	# 		raise forms.ValidationError("Cannot Be ABC")
	# 	return content



'''
Comments 

1. because while creating content, it even shows users to choose. but in reality it should not. 	

'''