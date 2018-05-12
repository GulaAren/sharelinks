from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import resolve
from urllib.parse import urlsplit

from .models import Link, Site

NUM_PER_PAGE = 7

def home(request):
	link_list = Link.objects.all().order_by('id')
	paginator = Paginator(link_list, NUM_PER_PAGE)
	
	page = request.GET.get('page')
	links = paginator.get_page(page)
	
	return render(request, 'home.html', {'links': links})

@login_required
def tambah(request):
	if request.method == 'POST':
		if 'url' not in request.POST.keys() or \
				'title' not in request.POST.keys():
			return redirect('post:home')
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
	if request.method == 'GET':
		if request.GET.get('next'):
			return redirect(request.GET.get('next'))
	return redirect('post:home')

def site_links(request, site_name):
	site = Site.objects.get(domain=site_name)
	link_list = site.link_set.all().order_by('id')
	# Pagination
	paginator = Paginator(link_list, NUM_PER_PAGE)
	page  = request.GET.get('page')
	links = paginator.get_page(page)
	
	return render(request, 'site.html', {
		'site': site,
		'links': links,
	})
