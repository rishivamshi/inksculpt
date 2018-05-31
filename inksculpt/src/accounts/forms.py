from django import forms

from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()

class UserRegisterForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	first_name = forms.CharField(max_length = 30)
	last_name = forms.CharField(max_length = 30)
	password = forms.CharField(widget = forms.PasswordInput)
	password2 = forms.CharField(label ='Confirm Password',  widget = forms.PasswordInput)

	
			

	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if password != password2:
			raise forms.ValidationError("Passwords must match")
		return password2

	def clean_username (self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__icontains = username).exists():
			raise forms.ValidationError(" This username is taken ")
		return username

	def clean_email (self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__icontains = email).exists():
			raise forms.ValidationError(" This email is already registered ")
		return email

class UserProfileModelForm(forms.ModelForm):
	
	
	class Meta:
		model = UserProfile
		fields = [
			"user", #1
			"profile_image",
			"cover_image",
			"dob",
			"gender",
			"city",
			"country",
			"status",
			"phone_number",

		]