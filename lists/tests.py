from django.test import TestCase
from django.urls import resolve

from lists import views


class HomePageTest(TestCase):

    def test_root_url_respolves_to_home_page_view(self):
        # resolve method shows what view is mapped to url
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)
