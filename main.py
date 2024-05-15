from autocorrect import Speller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


def itemsDict():
    spell = Speller(only_replacements=True)
    choice = 'yes'
    items = {}
    while choice == 'yes':
        item = spell(input("Item: ").title())
        correct = input(f"Did you mean {item}? ")
        if correct == "y" or "yes":
            amount = input("Amount: ")
            items[item] = amount
            choice = input("Add? (yes/no): ").lower()
    
    print (items)
    return items

# 1. create webscraper to get prices from the constr. websites and compare the best prices 
    # using selenium, scrape website for form id to input into selenium
    # use selenium to type in items into search bar 
    # scrape
    #  



# 2. create ui to allow user to write what they need and how much of it
# opt. what if they dont write the item properly? normalize using autocorrect
# 3. implement logic to give the user different options to shop all at one store, or a collection of stores if its cheaper
# 4. 
#  opt. make a gps navigation to the stores, (try to make it so they can put in their account info and reserve an order with pro desk, or normally online)

def main ():
    driver = webdriver.Chrome()

    stores = {
        1: {"HomeDep": {
            "url": "https://www.homedepot.ca/en/home.html",
            "id": "id5208"
        }},
        2: {"Rona": {
            "url": "https://www.rona.ca/en",
            "id": "search-input"
        }},
        3: {"HomeHar": {
            "url": "https://www.homehardware.ca/en",
            "id": "keywords"
        }}
    }

    items = {"wood": "12"}

    for q, item in enumerate(items):
        print (item, q)
        for store in stores.values():
            for name, details in store.items():
                driver.get(details['url'])

                try:
                    search_box = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID, details['id']))
                    )
                    search_box.send_keys(item)

                except NoSuchElementException:
                    print(f"Element with ID {details['id']} not found on the page {details['url']}.")
                finally:
                    driver.quit()

                # search_box.send_keys(item) 
                # search_box.submit()

                # time.sleep(5)

    

if __name__ == "__main__":
    main()