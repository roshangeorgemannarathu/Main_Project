

# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginformTest(LiveServerTestCase):

#     def testloginpage(self):
#         driver = webdriver.Firefox()

#         driver.get('http://127.0.0.1:8000/accounts/login/')

#         username_input = driver.find_element(By.NAME, 'username')
#         password_input = driver.find_element(By.NAME, 'password')
#         login_button = driver.find_element(By.NAME, 'submit')
#         username_input.send_keys('Roshangeorge')
#         password_input.send_keys('Roshangeorge')
#         login_button.click()  # Use click() instead of send_keys(Keys.RETURN) for the button click event

#         # Wait for the URL to contain '/home/' after successful login
#         WebDriverWait(driver, 10).until(EC.url_contains('http://127.0.0.1:8000/userloginhome/'))

#         # Assert specific elements or texts to ensure proper login
#         assert 'Pet Paradise Cart' in driver.page_source

#         # Close the WebDriver instance
#         driver.quit()


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginformTest(LiveServerTestCase):

    def testloginpage(self):
        # Use Chrome WebDriver
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/login/')

        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.NAME, 'submit')
        username_input.send_keys('testuser1')
        password_input.send_keys('Tes123@')
        login_button.click()  # Use click() instead of send_keys(Keys.RETURN) for the button click event

        # Wait for the URL to contain '/home/' after successful login
        WebDriverWait(driver, 10).until(EC.url_contains('/home/'))

        # Assert specific elements or texts to ensure proper login
        assert 'Welcome to SkillSwap' in driver.page_source

        # Close the WebDriver instance
        driver.quit()

