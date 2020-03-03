from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import generic
from urllib.parse import urlsplit

from .models import Link, Site


NUM_PER_PAGE = 25


class HomeView(generic.ListView):
    context_object_name = 'links'
    paginate_by = NUM_PER_PAGE
    model = Link
    template_name = 'home.html'

    def get_queryset(self):
        return Link.objects.all().order_by('-added_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TopView(generic.ListView):
    context_object_name = 'links'
    paginate_by = NUM_PER_PAGE
    model = Link
    template_name = 'top.html'

    def get_queryset(self):
        return Link.objects.all().order_by('-score')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
            site = None
            try:
                site = Site.objects.get(domain=netloc)
            except Exception:
                site = Site(domain=netloc)
            site.save()
            link = Link(author=request.user, content=url,
                        title=title, site=site)
            # Creator can't vote his/her link
            link.voters.add(request.user)
            link.save()

    return redirect('post:home')


@login_required
def vote(request, link_id):
    user = request.user
    link = Link.objects.get(id=link_id)
    if user not in link.voters.all():
        link.score += 1
        link.voters.add(user)
        link.save()
    if request.method == 'GET':
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
    return redirect('post:home')


def site_links(request, site_name):
    site = Site.objects.get(domain=site_name)
    link_list = site.link_set.all().order_by('-added_time')
    # Pagination
    paginator = Paginator(link_list, NUM_PER_PAGE)
    page = request.GET.get('page')
    links = paginator.get_page(page)

    return render(request, 'site.html', {
        'site': site,
        'links': links,
        'page_obj': links
    })


def user_links(request, username):
    user = User.objects.get(username=username)
    link_list = user.link_set.all().order_by('-added_time')
    # Pagination
    paginator = Paginator(link_list, NUM_PER_PAGE)
    page = request.GET.get('page')
    links = paginator.get_page(page)

    return render(request, 'user.html', {
        'user': user,
        'links': links,
        'page_obj': links
    })
