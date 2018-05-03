from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.db.utils import IntegrityError
from urllib.parse import urlsplit
#from django.utils.http
#from django.utils.encoding import 

class Site(models.Model):
	"""
	Submitted domain names
	"""
	# https://tools.ietf.org/html/rfc1034#section-3
	# max domain name octets is 255
	# subdomain ?
	domain = models.CharField(
		max_length=255, 
		unique=True
	)
	title = models.CharField(max_length=127, blank=True)
	score = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.domain

class Base(models.Model):
	title = models.CharField(max_length=127)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		abstract = True

	def __str__(self):
		return self.title

class Link(Base):
	"""
	URL as content, just that
	"""
	content = models.URLField()
	site = models.ForeignKey(Site, null=True,
		on_delete=models.CASCADE
	)
	score = models.PositiveIntegerField(default=0)

@receiver(post_save, sender=Link)
def create_site_link_list(sender, instance, created, **kwargs):
	if created:	
		try:
			netloc = urlsplit(sender.content).netloc	
			Site.objects.create(domain=netloc)
			instance.site.save()
		except: # IntegrityError:
			pass
