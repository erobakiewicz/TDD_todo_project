from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists import views
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_respolves_to_home_page_view(self):
        # resolve method shows what view is mapped to url
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_age_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
