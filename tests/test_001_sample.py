import pytest
from selenium.common.exceptions import TimeoutException

# from pages import page classes

import logging
from utils import copy_logs
import time


class TestSample1:

		@pytest.mark.smoke
    def test_001_01_sample_test_one(self, driver):
        # instantiate the pages
        sample_page = SamplePage(driver)
        
        # call the page methods
        # SamplePage.sample_method()
        
        logging.info('       :::::::::::: The action of the page method was executed :::::::::::: ')
        
        # at the end of the test copy the test log to the logs file
        copy_logs.append_log(source_log='logs/testing_log.txt', destination_log='logs/logs.txt')
      
        logging.info('                              :::::  Logs copied  :::::')