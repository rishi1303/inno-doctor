import unittest
from selenium.webdriver.common.keys import Keys
import HtmlTestRunner
from base import Baseconfig
from config import Configuration
import time
from selenium.webdriver.support.select import Select
class ViewProblemList(unittest.TestCase):

    def setUp(self):
        Baseconfig.driver.get(Configuration.BASE_URL)

        
    def test_viewproblemlist(self):

        actual_url='http://0.0.0.0:8000/patient_records/patient-problem-list-view/923412347235'
        Baseconfig.driver.find_element_by_xpath('//*[@id="navigation"]/ul/li[3]/a').click()
        Baseconfig.driver.find_element_by_id('id_email').send_keys(Configuration.USER_EMAIL)
        time.sleep(3)
        Baseconfig.driver.find_element_by_id('id_password').send_keys(Configuration.USER_PASSWORD)
        Baseconfig.driver.find_element_by_xpath('//*[@id="rememberMe"]').click()
        time.sleep(3)
        button=Baseconfig.driver.find_element_by_id('doctor_signin')
        Baseconfig.driver.execute_script("arguments[0].click();", button)
        time.sleep(3)

        checkpatient=Baseconfig.driver.find_element_by_xpath('//*[@id="navigation"]/ul/li[1]/a/p')
        Baseconfig.driver.execute_script("arguments[0].click();", checkpatient)
      
        element=Baseconfig.driver.find_element_by_name("aadhaarId")
        element.send_keys('923412347235')
        element.send_keys(Keys.ENTER)

        problemlistview= Baseconfig.driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div/div/div/ul/li[2]/a')
        Baseconfig.driver.execute_script("arguments[0].click();", problemlistview)
        
        expected_url = Baseconfig.driver.current_url
        self.assertEqual(actual_url, expected_url)
        Baseconfig.driver.quit()


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_dir'))