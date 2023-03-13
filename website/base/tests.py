from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from base.views import *


# Create your tests here.
class TestUrls(SimpleTestCase):

    def test_index_page_url_is_resolved(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEqual(resolve(url).func, index)

    def test_test_page_url_is_resolved(self):
        url = reverse('test')
        print(resolve(url))
        self.assertEqual(resolve(url).func, test)

    def test_speakers_page_url_is_resolved(self):
        url = reverse('speakers')
        print(resolve(url))
        self.assertEqual(resolve(url).func, speakers)

    def test_terms_and_conditions_page_url_is_resolved(self):
        url = reverse('terms_and_conditions')
        print(resolve(url))
        self.assertEqual(resolve(url).func, terms_and_conditions)

    def test_privacy_policy_page_url_is_resolved(self):
        url = reverse('privacy_policy')
        print(resolve(url))
        self.assertEqual(resolve(url).func, privacy_policy)

    def test_get_in_touch_page_url_is_resolved(self):
        url = reverse('get_in_touch')
        print(resolve(url))
        self.assertEqual(resolve(url).func, get_in_touch)

    def test_launch_your_speaking_event_page_url_is_resolved(self):
        url = reverse('launch_your_speaking_event')
        print(resolve(url))
        self.assertEqual(resolve(url).func, launch_your_speaking_event)
