from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		#checking that resolve, when called with "/", the root of the site, finds a function called home_page
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		#this is what Django will see when a user's browser asks for a page
		request = HttpRequest()
		#pass this request to our home_page view
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertIn('A new list item', response.content.decode())
		expected_html = render_to_string('home.html',{'new_item_text': 'A new list item'}
			)
		self.assertEqual(response.content.decode(), expected_html)