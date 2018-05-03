from django.contrib import admin

from .models import Link, Site


class LinkAdmin(admin.ModelAdmin):
	fields = ['title', 'author', 'content']

admin.site.register(Link, LinkAdmin)
admin.site.register(Site)