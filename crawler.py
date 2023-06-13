from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from find_banner import find_banner
import logging
import pandas as pd

def crawl(driver, selectors, sites, accept_words_list, deny_words_list, data):

    df = pd.DataFrame(data, index=[0])

    for index, site in enumerate(sites):
        try:
            logging.info('Trying site: ' + site)
            driver.get(site)
            logging.info('Sleeping for 3 seconds')
            sleep(3)
        except Exception:
            logging.exception("An exception was thrown while loading the site:")
        try:
            #Find the element that contains accept word
            logging.info('Finding consent element...')
            (accept_found,accept_type,accept_text) = find_banner(driver,selectors,accept_words_list)

            #If not found, switch to iframes and try again
            if not accept_found:
                iframes = driver.find_elements(By.CSS_SELECTOR, "iframe")
                logging.info('No initial consent element found, now looking in iframes...')
                for iframe in iframes:
                    driver.switch_to.frame(iframe)
                    logging.info('Switched to iframe: ' + str(iframe))
                    (accept_found,accept_type,accept_text) = find_banner(driver,selectors,accept_words_list)
                    driver.switch_to.default_content()

            if not accept_found:
                logging.info('No consent element could be found')

            #Find the element that contains the reject word
            logging.info('Finding reject element...')
            (reject_found,reject_type,reject_text) = find_banner(driver,selectors,deny_words_list)

            #If not found, switch to iframes and try again
            if not reject_found:
                iframes = driver.find_elements(By.CSS_SELECTOR, "iframe")
                logging.info('No initial reject element found, now looking in iframes...')
                for iframe in iframes:
                    driver.switch_to.frame(iframe)
                    logging.info('Switched to iframe: ' + str(iframe))
                    (reject_found,reject_type,reject_text) = find_banner(driver,selectors,deny_words_list)
                    driver.switch_to.default_content()

            if not reject_found:
                logging.info('No reject element could be found')

            #Making a screenshot
            logging.info('Sleeping for one second')
            sleep(1)
            logging.info('Making screenshot')
            driver.save_screenshot('screenshots/' + str(index) + '.png')

            #Adding info to dataframe
            new_entry = {'index': index, 'url': site, 'accept-found': accept_found, 'accept-type': accept_type, 'accept-text': accept_text, 
                            'reject-found': reject_found, 'reject-type': reject_type, 'reject-text': reject_text, 'error': False}
            new_df = pd.DataFrame(new_entry, index=[0])
            df = pd.concat([df, new_df], ignore_index=True)
        except Exception:
            logging.exception("An exception was thrown while crawling the site:")
            new_entry = {'index': index, 'url': site, 'accept-found': accept_found, 'accept-type': accept_type, 'accept-text': accept_text, 
                         'reject-found': reject_found, 'reject-type': reject_type, 'reject-text': reject_text, 'error': True}
            new_df = pd.DataFrame(new_entry, index=[0])
            df = pd.concat([df, new_df], ignore_index=True)
    
    return(df)
