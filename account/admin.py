from django.contrib import admin

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	fields = ('user', 'gender', 'birth_date', 'photo_profile')

admin.site.register(Profile, ProfileAdmin)
