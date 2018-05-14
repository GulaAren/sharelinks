from django.urls import path

from . import views

app_name = 'post'
urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('top', views.TopView.as_view(), name='top'),
	path('tambah', views.tambah, name='tambah'),
	path('vote/<int:link_id>', views.vote, name='vote'),
	path('site/<str:site_name>', views.site_links, 
		 name='site'),
	path('user/<str:username>', views.user_links, 
		 name='user'),
]