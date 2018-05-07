from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import (
	UserCreationForm,
	AuthenticationForm
)
from django.shortcuts import render, redirect

def daftar(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			return redirect('post:home')

	form = UserCreationForm()
	return render(request, 'daftar.html' ,{'form':form})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, 
							username=username,
							password=password)
		auth_login(request, user)
		if request.user.is_authenticated:
			if request.POST.get('next'):
				return redirect(request.POST.get('next'))
			return redirect('post:home')

	form = AuthenticationForm()
	if request.GET.get('next'):
		return render(request, 'login.html', {
			'form': form, 
			'next_url': request.GET.get('next'),
		})
	return render(request, 'login.html', {'form': form})

def logout(request):
	auth_logout(request)
	return redirect('post:home')
