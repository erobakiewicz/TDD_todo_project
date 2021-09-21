from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # checks specific URL
        self.browser.get('http://localhost:8000')
        # checks if title or header of the site mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        # fail - makes test fail no matter what here used to show message
        self.fail("Finish the test!")


# checks if script was run by shell not imported to another script
if __name__ == "__main__":
    unittest.main(warnings='ignore')
