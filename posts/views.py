from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from urllib.parse import urlsplit

from .models import Link, Site

def home(request):
	links = Link.objects.all()
	return render(request, 'home.html', {'links': links})

@login_required
def tambah(request):
	if request.method == 'POST':
		if 'url' not in request.POST.keys() or \
				'title' not in request.POST.keys():
			return redirect('home')
		url = request.POST['url']
		title = request.POST['title']
		netloc = urlsplit(url).netloc
		if not netloc:
			return redirect('post:home')
		if request.user.is_authenticated:
			site=None
			try:
				site = Site.objects.get(domain=netloc)
			except:
				site = Site(domain=netloc)
			site.save()
			Link(author=request.user, content=url,
				 title=title, site=site).save()

	return redirect('post:home')

@login_required
def vote(request, link_id):
	user = request.user
	link = Link.objects.get(id=link_id)
	if not user in link.voters.all():
		link.score += 1
		link.voters.add(user)
		link.save()
	return redirect('post:home')

def site_links(request, site_name):
	site = Site.objects.get(domain=site_name)
	return render(request, 'site.html', {'site': site})
