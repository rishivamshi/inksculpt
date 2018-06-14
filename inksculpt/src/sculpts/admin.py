from django.contrib import admin




# to replace admin form with SculptModelForm
from .forms import SculptModelForm

# Register your models here.
from .models import Sculpt

# we do this to register it into the admin page. so that we can look at the database.
#admin.site.register(Sculpt)

class SculptModelAdmin(admin.ModelAdmin):
	#form = SculptModelForm
	
	class Meta:
		model = Sculpt
		

admin.site.register(Sculpt, SculptModelAdmin)

