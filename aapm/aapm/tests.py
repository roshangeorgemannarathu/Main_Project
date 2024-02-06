from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class Hosttest(TestCase):
    
    def setUp(self):
        # Get the current directory of tests.py and construct the path to chromedriver.exe
        current_directory = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(current_directory, 'chromedriver.exe')

        # Initialize the webdriver without specifying executable_path
        self.driver = webdriver.Chrome(chromedriver_path)
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)

        # Use a more general CSS selector for the login link
        login = driver.find_element(By.CSS_SELECTOR, "a[href*='/accounts/login/']")
        login.click()
        time.sleep(2)

        username = driver.find_element(By.CSS_SELECTOR, "input#username.form-control[name='username'][required]")
        username.send_keys("Roshangeorge")
        password = driver.find_element(By.CSS_SELECTOR, "input#password.form-control[name='password'][required]")
        password.send_keys("Roshan@2k")
        time.sleep(2)

        submit = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")
        submit.click()
        time.sleep(2)

        # Click any image (you need to update the CSS selector based on your HTML structure)
        image = driver.find_element(By.CSS_SELECTOR, "img.sample-image")
        image.click()
        time.sleep(2)

        # Click the "Add to Cart" button (update the CSS selector)
        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, "button.btn-add-to-cart")
        add_to_cart_button.click()
        time.sleep(2)
