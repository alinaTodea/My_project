import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Login(unittest.TestCase):
    def setUp(self):
        self.driver = By.Chrome()  # Poți înlocui cu driverul preferat (Firefox, etc.)
        self.driver.get("https://the-internet.herokuapp.com/")
        self.driver.find_element(By.LINK_TEXT, "Form Authentication").click()

    def tearDown(self):
        self.driver.quit()

    def test_1_verify_url(self):
        expected_url = "https://the-internet.herokuapp.com/login"
        self.assertEqual(self.driver.current_url, expected_url)

    def test_2_verify_page_title(self):
        expected_title = "The Internet"
        self.assertEqual(self.driver.title, expected_title)

    def test_3_verify_heading_text(self):
        expected_text = "Login Page"
        heading = self.driver.find_element(By.XPATH, "//h2")
        self.assertEqual(heading.text, expected_text)

    def test_4_verify_login_button_displayed(self):
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertTrue(login_button.is_displayed())

    def test_5_verify_link_href_attribute(self):
        expected_href = "http://elementalselenium.com/"
        link = self.driver.find_element(By.LINK_TEXT, "Elemental Selenium")
        self.assertEqual(link.get_attribute("href"), expected_href)

    def test_6_verify_error_displayed_empty_credentials(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = self.driver.find_element(By.ID, "flash")
        self.assertTrue(error_message.is_displayed())

    def test_7_verify_error_message_with_invalid_credentials(self):
        expected_error_message = "Your username is invalid!"
        self.driver.find_element(By.ID, "username").send_keys("invalid")
        self.driver.find_element(By.ID, "password").send_keys("invalid")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = self.driver.find_element(By.ID, "flash").text
        self.assertTrue(expected_error_message in error_message,
                        "Error message text is incorrect")

    def test_8_verify_error_disappears_after_close(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".close").click()
        error_message = self.driver.find_elements(By.ID, "flash")
        self.assertEqual(len(error_message), 0)

    def test_9_verify_labels_text(self):
        expected_labels = ["Username", "Password"]
        labels = self.driver.find_elements(By.XPATH, "//label")
        actual_labels = [label.text for label in labels]
        self.assertListEqual(actual_labels, expected_labels)

    def test_10_verify_successful_login(self):
        expected_url = "https://the-internet.herokuapp.com/secure"
        self.driver.find_element(By.ID, "username").send_keys("validuser")
        self.driver.find_element(By.ID, "password").send_keys("validpass")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.assertIn(expected_url, self.driver.current_url)

        wait = unittest(self.driver, 10)
        success_message = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "flash.success"))
        )
        self.assertTrue(success_message.is_displayed())
        self.assertIn("secure area!", success_message.text)

    def test_11_verify_logout(self):
        self.driver.find_element(By.ID, "username").send_keys("validuser")
        self.driver.find_element(By.ID, "password").send_keys("validpass")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        expected_url = "https://the-internet.herokuapp.com/login"
        self.assertEqual(self.driver.current_url, expected_url)


if __name__ == "__main__":
    unittest.main()