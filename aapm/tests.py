# from django.contrib.auth.models import User
# from django.test import LiveServerTestCase
# from django.urls import reverse
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# import time
# class LoginTest(LiveServerTestCase):
#     def setUp(self):
#         self.driver  = webdriver.Chrome()
#     def tearDown(self):
#         self.driver.quit()
#     def test_login(self):
#         expected_url = 'http://127.0.0.1:8000/userloginhome/' 
#         print('Testing Started')
#         self.driver.get('http://127.0.0.1:8000/accounts/login/')
        
#         email_field = self.driver.find_element("id", "username")
#         password_field = self.driver.find_element("id","password")
#         email_field.send_keys('Hashim')
#         password_field.send_keys('H@$h1m001')
#         submit = self.driver.find_element("id","log_sub")
#         submit.click()
#         current_url = self.driver.current_url
#         print(current_url)
#         print(expected_url)
#         self.assertEqual(current_url, expected_url)





from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class AddDeliveryManTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        
    def tearDown(self):
        self.driver.quit()
        
    def test_add_delivery_man(self):
        # Assuming there's a user with credentials for testing login
        username = "admin"
        password = "admin"
        
        # Login first
        self.driver.get(self.live_server_url + '/accounts/login/')  
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("log_sub").click()
        
        # After successful login, proceed to add a deliveryman
        # expected_url = self.live_server_url + '/admin_dashboard/'  
        self.driver.get(self.live_server_url + '/add_delivery_man/')
        
        # Fill in deliveryman details
        self.driver.find_element_by_id("name").send_keys("Roshan George")
        self.driver.find_element_by_id("email").send_keys("roshangeorge2k66@gmail.com")
        self.driver.find_element_by_id("phone").send_keys("+919207483873")
        self.driver.find_element_by_id("house_name").send_keys("Mannarathu")
        
        # Select options from dropdowns
        district_dropdown = Select(self.driver.find_element_by_id("district"))
        district_dropdown.select_by_visible_text("Thiruvananthapuram")
        
        # Wait for cities and pincodes to populate
        time.sleep(1)  # Add a wait to ensure options are populated
        
        city_dropdown = Select(self.driver.find_element_by_id("city"))
        city_dropdown.select_by_visible_text("Thiruvananthapuram")
        
        pincode_dropdown = Select(self.driver.find_element_by_id("pincode"))
        pincode_dropdown.select_by_visible_text("695001")
        
        # Select vehicle type
        vehicle_dropdown = Select(self.driver.find_element_by_id("vehicle_type"))
        vehicle_dropdown.select_by_visible_text("Bike")
        
        self.driver.find_element_by_id("vehicle_no").send_keys("KL12AB1234")
        
        # Submit the form
        self.driver.find_element_by_id("adddel").click()  # Changed to use the ID provided in the HTML
        
        # Check if redirected to the expected URL after form submission
        # current_url = self.driver.current_url
        self.driver.get(self.live_server_url + '/admin_dashboard/')


if __name__ == '__main__':
    unittest.main()
