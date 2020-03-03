from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from . import views
from . import models


class HomeViewTests(TestCase):
    def test_home_view(self):
        url = reverse('post:home')
        response = self.client.get(url)
        # Link object is None
        self.assertEquals(response.status_code, 200)

    def test_home_url(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, views.HomeView)


class LinkViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            password="testpass"
        )
        models.Link.objects.create(
            title="Django Web Framework",
            author=self.user,
            content="https://www.djangoproject.com/"
        )

    def test_create_link_post(self):
        pass
        #self.client.post()
