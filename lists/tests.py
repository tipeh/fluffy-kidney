from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page, add_item_to_list
from django.http import HttpRequest

from lists.models import Item, List

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text':'A new list item'}
        )
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,"A new list item")


    def test_redirects_after_post(self):
        response = self.client.post(
            "/lists/new",
            data={'item_text':'A new list item'}
        )
        list_ = List.objects.first()
        self.assertRedirects(response,'/lists/%d/' % (list_.id))


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "Item 1"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item 2"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "Item 1")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item 2")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get("/lists/%d/" % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=list_)
        Item.objects.create(text="itemey 2", list=list_)
        other_list = List.objects.create()
        Item.objects.create(text="itemey 3", list=other_list)
        Item.objects.create(text="itemey 4", list=other_list)

        response = self.client.get("/lists/%d/" % (list_.id,))

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "itemey 3")
        self.assertNotContains(response, "itemey 4")

class AddItemToListTest(TestCase):

    def test_add_item_url_resolves_to_add_item_view(self):
        list_ = List.objects.create()
        found = resolve("/lists/(%d)/add_item" % (list_.id,))
        self.assertEqual(found.func, add_item_to_list)


    def test_can_add_items_to_existing_list(self):
        list_ = List.objects.create()
        item_to_add = "my new item"
        response = self.client.post(
            '/lists/%d/add_item' % (list_.id,),
            data={'item_text':"my new item"}
        )
        first_item = Item.objects.first()
        self.assertEqual(first_item.text, item_to_add)
        self.assertEqual(first_item.list, list_)

    def test_add_to_list_view_redirects_after_post(self):
        list_ = List.objects.create()
        response = self.client.post(
            "/lists/%d/add_item" % (list_.id,),
            data={"item_text":"Item added"}
        )
        self.assertRedirects(response,"lists/%d/" % (list_.id,))