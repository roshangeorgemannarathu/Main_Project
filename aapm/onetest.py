from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.driver  = webdriver.Chrome()
    def tearDown(self):
        self.driver.quit()
    def test_login(self):
        expected_url = 'http://127.0.0.1:8000/' 
        print('Testing Started')
        self.driver.get('http://127.0.0.1:8000//accounts/login/')
        
        self.driver.find_element("id", "id_login")
        email_field = self.driver.find_element("id", "id_login")
        password_field = self.driver.find_element("id","id_password")
        email_field.send_keys('snehajose2024b@mca.ajce.in')
        password_field.send_keys('!Mynameis22')
        submit = self.driver.find_element("id","log_sub")
        submit.click()
        current_url = self.driver.current_url
        print(current_url)
        print(expected_url)
        self.assertEqual(current_url, expected_url)

