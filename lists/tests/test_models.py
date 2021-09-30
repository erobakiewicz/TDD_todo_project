from unittest import TestCase

from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from lists.models import Item, List


class ListandItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.last()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 3)

        first_item_saved = saved_items[1]
        second_item_saved = saved_items[2]
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
