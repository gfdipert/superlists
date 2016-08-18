from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

# Create your tests here.
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		#chhoecking that resolve, when called with "/", the root of the site, finds a function called home_page
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		#this is what Django will see when a user's browser asks for a page
		request = HttpRequest()
		#pass this request to our home_page view
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	""" def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		#.method and .POST are special attributes of the HttpRequest
		#request.POST is a dictionary-like object containing all given HTTP POST parameters
		response = home_page(request)

		#testing that the view saves a new item to the database
		self.assertEqual(Item.objects.count(), 1)"""

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'],'/lists/the-only-list-in-the-world/')

	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(),0)

	"""def test_home_page_displays_all_list_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		request = HttpRequest()
		response = home_page(request)

		self.assertIn('itemey 1', response.content.decode())
		self.assertIn('itemey 2', response.content.decode())"""

class ListViewTest(TestCase):

	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list=list_)
		Item.objects.create(text='itemey 2', list=list_)

		#Django test client an attribute of Django TestCase, we tell it to .get the URL we're testing instead of calling the view function directly
		response = self.client.get('/lists/the-only-list-in-the-world/')

		#Django provides assertContains method which knows how to deal with responses and bytes of their content
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

class ListAndItemModelsTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)


