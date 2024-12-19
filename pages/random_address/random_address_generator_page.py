from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
import re


class RandomAddressGeneratorPage(BasePage):

    __url = 'https://zip.postcodebase.com/random_address_generator'

    # Locators
    __dropdowns_section_title = (By.XPATH, '//h2[text()="Random Address Generator"]')
    __dropdown_state = (By.XPATH, '//select[@id="StateSelect"]')
    __dropdown_city_index = (By.XPATH, '//select[@id="CityIndex"]')
    __dropdown_city_name = (By.XPATH, '//select[@id="CitySelect"]')
    __random_adresses = (By.XPATH, '//div[@id="randData"]//p')
    __msg_loading_success = (By.XPATH, '//p[@id="StatusString" and text()="Loading Success"]')


    # constructor
    def __init__(self, driver: webdriver):
        super().__init__(driver)

    
     # method to open the page
    def navigate_to_url_in_new_tab(self):
        super()._open_new_tab(self.__url)


    # method to switch back to main tab
    def switch_tab(self):
        super()._switch_to_main_tab()


    # method to switch back to main tab
    def close_tab(self):
        super()._close()

    
    # method to navivate to dropdowns section
    def scroll_to_random_generator_section(self):
        super()._scroll_to_element(self.__dropdowns_section_title)

    
    # method to get the state
    def get_state_name(self) -> str:
        state = super()._get_selected_option(self.__dropdown_state)
        state_name = re.findall(r'\(([^)]+)\)', state)
        state_name = state_name[0]
        # Newhampshire is misspelled on the random address page
        if state_name == 'Newhampshire':
            state_name = 'New Hampshire'
        return state_name
    

    # method to get the city
    def get_city_name(self) -> str:
        return super()._get_selected_option(self.__dropdown_city_name)
    

    # method to get the random adress list
    def get_adress(self) -> list:
        super()._select_dropdown_option(self.__dropdown_state)
        # wait until the cities are populated in the other dropdowns - until the msg Loading Success s displayed
        super()._wait_until_element_is_visible(self.__msg_loading_success)
        super()._select_dropdown_option(self.__dropdown_city_index)
        super()._select_dropdown_option(self.__dropdown_city_name)
        return super()._get_text_list(self.__random_adresses)
    

    # method to clean and create the adress list
    def random_address_list(self) -> list:
        
        adress_list = list()

        captured_adresses = self.get_adress()

        for address in captured_adresses:
            address = address.text
            address = address.split('/n')
            for line in address:
                line = line.replace('\n', ' ')
                line = line[:-3]
                adress_list.append(line)
        
        return adress_list
    

    # method to create an adress dict
    def random_address_dict(self) -> dict:
        
        adress_list = list()

        captured_adresses = self.get_adress()
        state_name = self.get_state_name()
        city_name = self.get_city_name()

        for address in captured_adresses:
            address = address.text
            if "PO BOX" in address:
                continue           
            address = address.split('/n')
            for line in address:
                line = line.replace('\n', '')
                line = line[:-3]
                adress_list.append(line)
        

        for address in adress_list:
            
            random_address_dict = dict()
            
            # clean the address
            
            # get the zip code
            zip_code = re.findall(r'[0-9]*[-][0-9]*', address)
            zip_code = zip_code[0]
            # validate if zip code is 'xxxxx-xxxx'
            zip_code_valid_pattern = r'^\d{5}-\d{4}$'
            if re.match(zip_code_valid_pattern, zip_code):
                pass
            else:
                # if the zip code does't match the 9 digit zip code > slice it to have only 5 digits 'xxxxx'
                zip_code = zip_code[:5]

            # remove the state and zip code from the address with re
            address_1 = re.sub(r'(\s...[0-9]*[-][0-9]*)', '', address)

            # remove the city with replace
            address_1 = address_1.replace(city_name, '')
            
            # add key/values to the dict
            random_address_dict['address'] = address_1.strip()
            random_address_dict['city'] = city_name
            random_address_dict['state'] = state_name
            random_address_dict['zip_code'] = zip_code
            logging.info(f"               {random_address_dict['address']}, {random_address_dict['city']}, {random_address_dict['state']}, {random_address_dict['zip_code']}")
            
            # check if the dictionary is not empty before returning the dict
            # to fix > UnboundLocalError: cannot access local variable 'random_address_dict' where it is not associated with a value
            if len(random_address_dict) != 0:
                break

        return random_address_dict
    

    # method to get a random address dict
    def get_random_address(self) -> dict:
        # 1 - open the paghe in a new tab 
        self.navigate_to_url_in_new_tab()
        # 2 - scroll to section
        self.scroll_to_random_generator_section()
        # 3 - get the address dict
        random_address = self.random_address_dict()
        # close the new tab
        self.close_tab()
        # switch to main tab
        self.switch_tab()

        return random_address
    
