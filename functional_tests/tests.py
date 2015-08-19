from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        print("Connecting to the URL")
        self.browser.get(self.live_server_url)


        # She notices the page title and header mention to-do lists
        print("Test : 'To-Do' in the title ?")
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        print("Test : 'To-Do' in the header ?")
        self.assertIn('To-Do',header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        edith_item_to_send_1 = 'Buy peacock feathers'
        print("Typing "+str(edith_item_to_send_1))
        input_box.send_keys(edith_item_to_send_1)


        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        print("Enter")
        input_box.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        print("Test : has been redirected to its own URL ?")
        self.assertRegex(edith_list_url,'lists/.+')
        print("Test : '1: "+edith_item_to_send_1+"' in the table ?")
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        # The page updates again, and now shows both items on her list
        input_box = self.browser.find_element_by_id("id_new_item")
        edith_item_to_send_2 = "Use peacock feathers to make a fly"
        print("Typing again '"+edith_item_to_send_2+"'")
        input_box.send_keys(edith_item_to_send_2)
        print("Enter")
        input_box.send_keys(Keys.ENTER)

        print("Test : the 2 rows exist and correctly numbered ?")
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        print("Edith quits...")
        self.browser.quit()

        import time
        time.sleep(2)

        print("A new user comes : Francis")
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        print("Test : did francis fall onto edith's items ?")
        self.assertNotIn(edith_item_to_send_1,page_text)
        self.assertNotIn(edith_item_to_send_2,page_text)

        input_box = self.browser.find_element_by_id("id_new_item")
        francis_new_item_1 = "Buy milk"
        print("Typing : '"+francis_new_item_1+"'")
        input_box.send_keys(francis_new_item_1)
        print("Enter")
        input_box.send_keys(Keys.ENTER)

        francis_url = self.browser.current_url
        print("Test : has been redirected to its iwn URL ?")
        self.assertRegex(francis_url, "/lists/.+")
        print("Test : ...not the same URL as edith's ?")
        self.assertNotEqual(francis_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        print("Test : is there any edith's element ?")
        self.assertNotIn(edith_item_to_send_1, page_text)
        self.assertNotIn(edith_item_to_send_2, page_text)


    def test_styling_and_layout(self):
        #Edith goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        #She notices the input is nicely centered
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"]/2,
                               512,
                               delta=5
                               )


        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                    inputbox.location['x'] + inputbox.size['width'] / 2,
                    512,
                    delta=5)

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])
