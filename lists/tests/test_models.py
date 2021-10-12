from django.test import TestCase
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from lists.models import Item, List


class ListAndItemModelsTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        list_.save()

        first_item = Item.objects.create(list=list_)
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item.objects.create(list=list_)
        second_item.text = "Item the second"
        second_item.save()

        saved_list = List.objects.last()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_item_saved = saved_items[0]
        second_item_saved = saved_items[1]
        self.assertEqual(first_item_saved.text, 'The first (ever) list item')
        self.assertEqual(first_item_saved.list, list_)
        self.assertEqual(second_item_saved.text, 'Item the second')
        self.assertEqual(second_item_saved.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
            return redirect(f'/lists/{list_.id}/')

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise
