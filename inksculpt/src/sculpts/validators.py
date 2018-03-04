from django.core.exceptions import ValidationError # for validation

# validation can be done in the forms also, but it will work only when the form comes up, not when the model comes up. meaning, working with model is universal.

# this where we can prevent profanity or use of bad words in the platform.

# for validation

def validate_content(value):
	content = value
	if content == "":
		raise ValidationError("content cannot be blank")
	return value

