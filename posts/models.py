from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models

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
	site = models.ForeignKey(
		Site, null=True,
		on_delete=models.CASCADE
	)
	score = models.PositiveIntegerField(default=0)
	voters = models.ManyToManyField(User, related_name="voter")
	added_time = models.DateTimeField(auto_now=True)