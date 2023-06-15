import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://the-internet.herokuapp.com/")
        self.driver.find_element(By.LINK_TEXT, "Form Authentication").click()

    def tearDown(self):
        self.driver.quit()

    def test_url(self):
        expected_url = "https://the-internet.herokuapp.com/login"
        actual_url = self.driver.current_url
        self.assertEqual(actual_url, expected_url, "URL is incorrect")

    def test_page_title(self):
        expected_title = "The Internet"
        actual_title = self.driver.title
        self.assertEqual(actual_title, expected_title, "Page title is incorrect")

    def test_heading_text(self):
        expected_text = "Login Page"
        actual_text = self.driver.find_element(By.XPATH, "//h2").text
        self.assertEqual(actual_text, expected_text, "Heading text is incorrect")

    def test_login_button_displayed(self):
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertTrue(login_button.is_displayed(), "Login button is not displayed")

    def test_elemental_selenium_link_href(self):
        expected_href = "http://elementalselenium.com/"
        link = self.driver.find_element(By.LINK_TEXT, "Elemental Selenium")
        actual_href = link.get_attribute("href")
        self.assertEqual(actual_href, expected_href, "Elemental Selenium link href is incorrect")

    def test_empty_credentials_error(self):
        self.driver.find_element(By.CSS_SELECTOR, "#username").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#password").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#login > button").click()
        error_message = self.driver.find_element(By.ID, "flash").text
        self.assertTrue("Your username is invalid!" in error_message, "Error message text is incorrect")

    def test_invalid_credentials_error(self):
        username_input = self.driver.find_element(By.CSS_SELECTOR, "#username")
        password_input = self.driver.find_element(By.CSS_SELECTOR, "#password")
        username_input.clear()
        password_input.clear()
        username_input.send_keys("invalid_user")
        password_input.send_keys("invalid_password")
        self.driver.find_element(By.CSS_SELECTOR, "#login > button").click()
        error_message = self.driver.find_element(By.ID, "flash").text
        expected_error_message = "Your username is invalid!"
        self.assertTrue(expected_error_message in error_message, "Error message text is incorrect")

    def test_dismiss_error_message(self):
        self.driver.find_element(By.CSS_SELECTOR, "#username").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#password").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#login > button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".flash > .close").click()
        error_message = self.driver.find_element(By.ID, "flash").text
        self.assertEqual(error_message, "", "Error message is still displayed after dismissing")

    def test_label_texts(self):
        expected_labels = ["Username", "Password"]
        labels = self.driver.find_elements(By.XPATH, "//label")
        actual_labels = [label.text for label in labels]
        self.assertListEqual(actual_labels, expected_labels, "Label texts are incorrect")

    def test_successful_login(self):
        username_input = self.driver.find_element(By.CSS_SELECTOR, "#username")
        password_input = self.driver.find_element(By.CSS_SELECTOR, "#password")
        username_input.clear()
        password_input.clear()
        username_input.send_keys("valid_user")
        password_input.send_keys("valid_password")
        self.driver.find_element(By.CSS_SELECTOR, "#login > button").click()
        expected_url = "https://the-internet.herokuapp.com/secure"
        actual_url = self.driver.current_url
        self.assertIn(expected_url, actual_url, "URL does not contain '/secure'")
        success_message = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "flash.success"))).text
        self.assertTrue(success_message.startswith("You logged into a secure area!"),
                        "Success message is incorrect")

    def test_logout(self):
        username_input = self.driver.find_element(By.CSS_SELECTOR, "#username")
        password_input = self.driver.find_element(By.CSS_SELECTOR, "#password")
        username_input.clear()
        password_input.clear()
        username_input.send_keys("valid_user")
        password_input.send_keys("valid_password")
        self.driver.find_element(By.CSS_SELECTOR, "#login > button").click()
        self.driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]").click()
        expected_url = "https://the-internet.herokuapp.com/login"
        actual_url = self.driver.current_url
        self.assertEqual(actual_url, expected_url, "Did not navigate to the login page")

if __name__ == "__main__":
    unittest.main()
