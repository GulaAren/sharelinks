from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase

from account.views import daftar, login, logout

class DaftarViewTests(TestCase):
	def setUp(self):
		self.url = reverse('daftar')
		self.response = self.client.get(self.url)

	def test_daftar_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_daftar_resolve(self):
		view = resolve(self.url)
		self.assertEquals(view.func, daftar)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, UserCreationForm)

class DaftarSuccessTest(TestCase):
	def setUp(self):
		self.url = reverse('daftar')
		data = {
			'username' : "testuser",
			'password1': "testpass",
			'password2': "testpass",
		}
		self.response = self.client.post(self.url, data)
		self.home_url = reverse('home')

	def test_redirect(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_logged_in(self):
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)


class DaftarFailTest(TestCase):
	def setUp(self):
		self.url = reverse('daftar')
		data = {}
		self.response = self.client.post(self.url, data)
		self.home_url = reverse('home')

	def test_daftar_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_user_not_created(self):
		self.assertFalse(User.objects.exists())

class LoginViewTest(TestCase):
	def test_daftar_status_code(self):
		resp = self.client.get(reverse('login'))
		self.assertEquals(resp.status_code, 200)

	def test_daftar_resolve(self):
		view = resolve(reverse('login'))
		self.assertEquals(view.func, login)

class LoginSuccessTest(TestCase):
	def setUp(self):
		self.url = reverse('login')
		data = {
			'username': "testuser",
			'password1': "testpass",
			'password2': "testpass",
		}
		url_daftar = reverse('daftar')
		self.client.post(url_daftar, data)
		data = {
			'username': "testuser",
			'password': "testpass",
		}
		self.response = self.client.post(self.url, data)
		self.home_url = reverse('home')

	def test_redirect(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_logged_in(self):
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

	def test_logout(self):
		response = self.client.get('logout')
		user = response.context.get('user')
		self.assertFalse(user)