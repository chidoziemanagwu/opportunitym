from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from users.views import *


# Create your tests here.
class TestUrls(SimpleTestCase):
    def test_index_page_url_is_resolved(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEqual(resolve(url).func, register)
