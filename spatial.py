from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import random

def close_dialog(driver):
    try:
        # Wait 50'' until the dialog box closes
        time.sleep(50)  # Change the seconds if necessary

        # This should find the close button on the screen
        close_button = driver.find_element(By.XPATH, "/html/body/div/span/div/div/div/div[1]/div[1]/div/div/div/div[2]/span/div/button")

        # Click on the close button
        close_button.click()
        print("Dialog closed successfully.")
        
    except Exception as e:
        print(f"An error occurred while trying to close the dialog: {e}")

def monitor_users(driver, metaverse_url, check_interval=5):
    driver.get(metaverse_url)
    close_dialog(driver) 
    while True:
        try:
            # Wait until the box "People" becomes visible. Change seconds if necessary
            WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'People')]"))
            )
            
            # Find number of people
            people_element = driver.find_element(By.XPATH, "//h2[contains(text(), 'People')]")
            
            # Take number of people
            people_text = people_element.text

            num_people = int(people_text.split("(")[1].split(")")[0])
            
            # Verify if there are more users
            if num_people > 1:
                print(f"Detected {num_people} people! Switching to a new metaverse...")
                # if more than 1 change metaverse
                switch_metaverse(driver)
            else:
                # wait to check again
                time.sleep(check_interval)

        except NoSuchElementException:
            print("Element 'People' not found. Ensure the XPath is correct.")
            time.sleep(check_interval)  # Wait to check again
        except Exception as e:
            print(f"An error occurred while checking the number of users: {e}")
            break

def switch_metaverse(driver):
    # This is the list of metaverse urls, just as an example
    metaverse_urls = [
        "https://www.spatial.io/s/Connect-Convention-Center-63d995f7b41c7e480ca34822?share=736452377713008703",
        "https://www.spatial.io/s/2-22-StudioVerse-654691a9fd66b64b63cbadc8?share=3728236322333713537",
        "https://www.spatial.io/s/uCONSUMER-Home-Forge-651e59009f9634efe50a53f9?share=3752484812616474508"
    ]
    
    # Select random metaverse from list
    new_metaverse_url = random.choice(metaverse_urls)
    
    # Change to new metaverse
    driver.get(new_metaverse_url)
    close_dialog(driver)  # Close dialog box
    print(f"Switched to a new metaverse: {new_metaverse_url}")

def main():
    # Check driver
    service = Service('/usr/local/bin/geckodriver')  # change path to your geckodrive

    firefox_options = Options()

    # Create WebDriver for Firefox
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # URL of first metaverse
    initial_metaverse_url = "https://www.spatial.io/s/Ghost-Radio-Station-Whales-645d35c1de1c38ebc0c79b8b?share=3709427844976361071"

    try:
        # check if there are changes on the number of users
        monitor_users(driver, initial_metaverse_url)

    except Exception as e:
        print(f"An error occurred during initial setup: {e}")

    finally:
        # change browser when finished
        driver.quit()

if __name__ == "__main__":
    main()
