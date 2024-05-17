from autocorrect import Speller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import lxml

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def search_items(driver, store_details, items):
    for name, details in store_details.items():
        driver.get(details['url'])
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, details['search_selector']))
            )
            for item, quantity in items.items():
                search_box.clear()
                search_box.send_keys(item + Keys.RETURN)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, details['price_selector']))
                )
                prices = driver.find_elements(By.CSS_SELECTOR, details['price_selector'])
                print(f"Prices for {item} at {name}:")
                for price in prices:
                    print(price.text)
        except TimeoutException:
            print(f"Failed to load {name} properly.")
        except NoSuchElementException:
            print(f"Search box not found on {name}.")
        except Exception as e:
            print(f"Error in searching at {name}: {e}")


def getItems():
    spell = Speller(only_replacements=True)
    items = {}
    while True:
        item = input("Item: ").title()
        corrected_item = spell(item)
        correct = input(f"Did you mean {corrected_item}? (y/n): ").lower()
        if correct in ["y", "yes"]:
            amount = input("Amount: ")
            items[corrected_item] = amount
        if input("Add more items? (y/n): ").lower() not in ["y", "yes"]:
            break
    return items

# 1. create webscraper to get prices from the constr. websites and compare the best prices 
    # using selenium, scrape website for form id to input into selenium
    # use selenium to type in items into search bar 
# 2. create ui to allow user to write what they need and how much of it
# opt. what if they dont write the item properly? normalize using autocorrect
# 3. implement logic to give the user different options to shop all at one store, or a collection of stores if its cheaper
# 4. 
#  opt. make a gps navigation to the stores, (try to make it so they can put in their account info and reserve an order with pro desk, or normally online)

def main():
    items = getItems()
    if not items:
        print("No items to search.")
        return
    
    driver = setup_driver()

    store_details = {
        "HomeDepot": {
            "url": "https://www.homedepot.ca/en/home.html",
            "search_selector": "input.acl-input[placeholder='What can we help you find?']",
            "price_selector": ".price__numbers"
        # },
        # "Rona": {
        #     "url": "https://www.rona.ca/en",
        #     "search_selector": "#search-input",
        #     "price_selector": ".product-price"
        # },
        # "HomeHardware": {
        #     "url": "https://www.homehardware.ca/en",
        #     "search_selector": "#keywords",
        #     "price_selector": ".product-price"
        }
    }
    
    search_items(driver, store_details, items)

    driver.quit()



if __name__ == "__main__":
    main()



    # try:
    #     WebDriverWait(driver, 5).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cookie-consent-accept'))
    #     ).click()
    # except TimeoutException:
    #     print("No cookie pop-up or already handled.")

    # try:
    #     search_box = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, details['search_selector']))
    #     )
    #     search_box.clear()
    #     search_box.send_keys("2x4 wood")  # Example search term

    #     # Locate and click the search button using the button selector from the dictionary
    #     search_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, details['button_selector']))
    #     )
    #     search_button.click()
        
    #     WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.CSS_SELECTOR, details['price_selector']))
    #     )
        
    #     #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     #Extract prices

    #     for item, quantity in items.items():
    #         price_elements = driver.find_elements(By.CSS_SELECTOR, details['price_selector'])
    #         for price_element in price_elements:
    #             try:
    #                 price = price_element.text
    #                 print(f"Price at {name}: {price}")

    #             except Exception as e:
    #                 print(f"Error in extracting prices at {name}: {e}")
    # except Exception as e:
    #     print(f"Error in searching at {name}: {e}")