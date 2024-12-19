"""
BASE PAGE
with all the methods that are common to all the pages
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import random
import logging


class BasePage:

    # constructor
    def __init__(self, driver: WebDriver):
        self._driver = driver


    # method to open the url
    def _open(self, url):
        self._driver.get(url)

    # method to open the url in a new tab
    def _open_new_tab(self, url):
        self._driver.execute_script(f'window.open("{url}");')
        self._driver.switch_to.window(self._driver.window_handles[1])


    # method to switch back to RL tab
    def _switch_to_main_tab(self):
        self._driver.switch_to.window(self._driver.window_handles[0])


    # method to close the browser
    def _close(self):
        self._driver.close()
    

    # method to find the element
    def _find(self, locator: tuple) -> WebElement:
        return self._driver.find_element(*locator)
    

    # method to find all the elements
    def _find_all(self, locator: tuple) -> WebElement:
        return self._driver.find_elements(*locator)
    

    # method to wait until the element is visible
    def _wait_until_element_is_visible(self, locator: tuple, time: int = 25):
        wait = WebDriverWait(self._driver, time)
        wait.until(ec.visibility_of_element_located(locator))
    

    # method to wait until the element is not visible
    def _wait_until_element_is_not_visible(self, locator: tuple, time: int = 25):
        wait = WebDriverWait(self._driver, time)
        wait.until(ec.invisibility_of_element_located(locator))


    # method to wait until the element is clickable
    def _wait_until_element_is_clickable(self, locator: tuple, time: int = 25):
        wait = WebDriverWait(self._driver, time)
        wait.until(ec.element_to_be_clickable(locator))


    # method to type text in input
    def _type(self, locator: tuple, text: str, time: int = 25):
        self._wait_until_element_is_visible(locator, time)
        self._find(locator).send_keys(text)


    # method to press ENTER in input
    def _press_enter_key_in_input(self, locator: tuple, time: int = 25):
        self._wait_until_element_is_visible(locator, time)
        self._find(locator).send_keys(Keys.ENTER)


    # method to press ENTER 
    def _press_enter_key(self):
        actions = ActionChains(self._driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()


    # method to get the text
    def _get_text(self, locator: tuple,time: int = 25) -> str:
        self._wait_until_element_is_visible(locator, time)
        return self._find(locator).text
    

    # method to get the all the text elements on a list
    def _get_text_list(self, locator: tuple,time: int = 25) -> list:
        self._wait_until_element_is_visible(locator, time)
        return self._find_all(locator)


    # method to get the innerText
    def _get_inner_text(self, locator: tuple,time: int = 25) -> str:
        self._wait_until_element_is_visible(locator, time)
        return self._find(locator).get_attribute('innerText') 


    # method to click on an element
    def _click(self, locator: tuple, time: int = 25):
        self._wait_until_element_is_visible(locator, time)
        #self._wait_until_element_is_clickable(locator, time)
        self._find(locator).click()


    # method to scroll to element
    def _scroll_to_element(self, locator: tuple, time: int = 50):
        element_to_scroll = self._find(locator)
        #self._driver.execute_script('arguments[0].scrollIntoView(true);', element_to_scroll) # using JavaScript and the scrollIntoView() is not working
        ActionChains(self._driver).move_to_element(element_to_scroll).perform()


    # method to verify if element is displayed
    def _is_displayed(self, locator: tuple) -> bool:
        try:
            return self._find(locator).is_displayed()
        except NoSuchElementException:
            return False
    

    # method to take a screenshot
    def _take_screenshot(self):
        self._driver.get_screenshot_as_file('screenshots/last_error.png')

    
    # method to get the selected value from dropdown
    def _get_selected_option(self, locator: tuple, time: int = 10) -> str:
        self._wait_until_element_is_visible(locator, time)
        dropdown = self._find(locator)
        select_option = Select(dropdown)
        return select_option.first_selected_option.text
    

    # method to select the random dropdown option
    def _select_dropdown_option(self, locator: tuple, time: int = 10):
        self._wait_until_element_is_visible(locator, time)
        dropdown = self._find(locator)
        select_option = Select(dropdown)
        # get the total number of options in the dropdown
        number_of_options = len(select_option.options)
        # select by random index
        select_option.select_by_index(random.randint(1, number_of_options - 1))
