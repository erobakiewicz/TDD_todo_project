from unittest import skip

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # user tries to add empty item to list by accident

        # page refreshes and there is a message that item cannot be blank

        # user adds item with content and it works

        # user tries again to add blank item and gets similar warining

        # user correct it by adding some content

        self.fail("Finish the test")
