from selenium.webdriver.common.by import By
import logging

def find_banner(driver,selectors,words_list):
    logging.info('Selecting elements to search')
    elements = driver.find_elements(By.CSS_SELECTOR, selectors)
    
    logging.info('Searching selected elements')
    for e in elements:
        if e.text.lower().strip(" ✓›!\n>") in words_list:
            driver.execute_script("arguments[0].style.border='4px solid red'", e)
            logging.info('Element found: ' + str(e.tag_name) + ' with text: ' + str(e.text.lower().strip(" ✓›!\n>")))
            return(True,str(e.tag_name),str(e.text.lower().strip(" ✓›!\n>")))
    return(False,'','')