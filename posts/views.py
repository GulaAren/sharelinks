from django.shortcuts import render

from .models import Link

def home(request):
	links = Link.objects.all()
	return render(request, 'home.html', {'links': links})

