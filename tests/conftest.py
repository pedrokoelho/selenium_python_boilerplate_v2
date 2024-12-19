import pytest
from selenium import webdriver


@pytest.fixture()
def driver():
    
    # setup
    options = webdriver.EdgeOptions() # EDGE
    #options = webdriver.ChromeOptions() # CHROME

    options.add_argument("--start-maximized")
    options.add_argument("InPrivate") # EDDGE

    my_driver = webdriver.Edge(options=options) # EDDGE
    #my_driver = webdriver.Chrome(options=options) # CHROME

    # run tests
    yield my_driver

    # teardown
    my_driver.quit()
