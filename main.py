from autocorrect import Speller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import time
chrome_options = webdriver.ChromeOptions()

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

def main():
    
    chrome_options.headless = False
    driver = webdriver.Chrome(options=chrome_options)  # Consider using a context manager or try/finally to ensure it closes
    
    stores = {
    1: {
        "HomeDep": {
            "url": "https://www.homedepot.ca/en/home.html",
            "search_selector": "input.acl-input[placeholder='What can we help you find?']",
            "button_selector": "button.acl-action-button.icon-button",  # Assuming 'acl-action-button' and 'icon-button' are enough to uniquely identify the button
            "price_selector": ".acl-product-card_price"
        }
    },
    # 2: {
    #     "Rona": {
    #         "url": "https://www.rona.ca/en",
    #         "search_selector": "#search-input",
    #         "button_selector": "button.search-button-class",  # Placeholder, update with actual button selector from Rona
    #         "price_selector": ".product-price"
    #     }
    # },
    # 3: {
    #     "HomeHar": {
    #         "url": "https://www.homehardware.ca/en",
    #         "search_selector": "#keywords",
    #         "button_selector": "button.search-submit-button",  # Placeholder, update with actual button selector from Home Hardware
    #         "price_selector": ".product-price"
    #     }
    }

    items = {"2x4 wood": 12}  # Assuming you want to look up 'wood', quantity '12'

    for store_key, store_value in stores.items():
        for name, details in store_value.items():
            driver.get(details['url'])
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cookie-consent-accept'))
                ).click()
            except TimeoutException:
                print("No cookie pop-up or already handled.")

            try:
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, details['search_selector']))
                )
                search_box.clear()
                search_box.send_keys("2x4 wood")  # Example search term

                # Locate and click the search button using the button selector from the dictionary
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, details['button_selector']))
                )
                search_button.click()
                
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, details['price_selector']))
                )
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #Extract prices

                for item, quantity in items.items():
                    price_elements = driver.find_elements(By.CSS_SELECTOR, details['price_selector'])
                    for price_element in price_elements:
                        try:
                            price = price_element.text
                            print(f"Price at {name}: {price}")

                        except Exception as e:
                            print(f"Error in extracting prices at {name}: {e}")
            except Exception as e:
                print(f"Error in searching at {name}: {e}")
    driver.quit()

if __name__ == "__main__":
    main()