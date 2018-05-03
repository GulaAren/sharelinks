from django.contrib import admin

from .models import Link


class LinkAdmin(admin.ModelAdmin):
	fields = ['title', 'author', 'site', 'content']

admin.site.register(Link, LinkAdmin)