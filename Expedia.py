import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import ssl
import logging
import os

ssl._create_default_https_context = ssl._create_unverified_context

# Setup logging
logging.basicConfig(filename='expedia_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create screenshots directory if it doesn't exist
screenshots_dir = 'screenshots'
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)

def save_screenshot(driver, step_name):
    """Save a screenshot in the 'screenshots' directory with a unique filename based on the step name."""
    filename = os.path.join(screenshots_dir, f"{step_name}_{int(time.time())}.png")
    driver.save_screenshot(filename)
    logging.info(f"Screenshot taken: {filename}")

if __name__ == "__main__":
    # Set up the WebDriver
    driver = uc.Chrome()

    try:
        # Navigate to the Expedia website
        driver.get("https://www.expedia.co.in/")
        save_screenshot(driver, "LandingPage")
        logging.info(f"URL: {driver.current_url}")
        logging.info(f"Title: {driver.title}")

        # Click on "Flights"
        flights_tab = driver.find_element(By.XPATH, "//a[.//span[text()='Flights']]")
        flights_tab.click()
        save_screenshot(driver, "FlightsTabClicked")
        logging.info('Flights tab clicked')

        # Click the button using the full XPath
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[4]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div[1]/button"))
        )
        button.click()
        save_screenshot(driver, "SearchButtonClicked")
        logging.info('Search button clicked')

        # Wait for the input field to become visible
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Leaving from']"))
        )

        # Enter "Kolkata" into the input field
        input_field.send_keys("Kolkata")
        input_field.send_keys(Keys.RETURN)
        save_screenshot(driver, "LeavingFromSet")
        logging.info("Leaving from set to Kolkata")

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//*[@id='FlightSearchForm_ROUND_TRIP']/div/div[1]/div/div[2]/div/div/div[2]/div[1]/button"))
        )
        button.click()
        save_screenshot(driver, "SearchButtonClickedAfterLeaving")
        logging.info('Search button clicked after setting Leaving From')

        # Wait for the input field to become visible
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Going to']"))
        )

        # Enter "Hyderabad" into the input field
        input_field.send_keys("Hyderabad")
        input_field.send_keys(Keys.RETURN)
        save_screenshot(driver, "GoingToSet")
        logging.info("Going to set to Hyderabad")

        # Click on the departure date picker
        departure_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='uitk-date-selector-input1-default']"))
        )
        departure_date.click()
        save_screenshot(driver, "DepartureDatePickerClicked")
        logging.info("Departure date picker clicked")

        # Wait for the calendar to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//table[@aria-label='September 2024']"))
        )
        logging.info("Calendar opened")

        # Select the date "September 8"
        target_date = "8"
        calendar_table = driver.find_element(By.XPATH, "//table[@aria-label='September 2024']")

        for cell in calendar_table.find_elements(By.CLASS_NAME, 'uitk-date-number'):
            if cell.text == target_date:
                cell.find_element(By.XPATH, './ancestor::td').click()
                break
        save_screenshot(driver, "DateSelected")
        logging.info("September 8 date selected")

        # Click on the "Done" button
        done_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//footer//button[@data-stid='apply-date-selector']"))
        )
        done_button.click()
        save_screenshot(driver, "DoneButtonClicked")
        logging.info("Done button clicked")

        # Click the button to open the traveler selector
        traveler_selector_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="FlightSearchForm_ROUND_TRIP"]/div/div[3]/div/div[1]/button'))
        )
        traveler_selector_button.click()
        save_screenshot(driver, "TravelerSelectorOpened")
        logging.info("Traveler selector opened")

        # Wait for the traveler selector to be visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[4]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div/div[3]/div/div[2]'))
        )

        increase_adult_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[4]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div/div[3]/div/div[2]/div/div/section/div[1]/div/div/button[2]')

        # Click the increase button to set adults to 2
        for _ in range(1):  # We need to click once to set it to 2
            increase_adult_button.click()
            time.sleep(0.5)  # Adjust this wait time if needed
        save_screenshot(driver, "AdultsIncreased")
        logging.info("Number of adults increased")

        # Locate the "Done" button and click it
        done_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[4]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div/div[3]/div/div[2]/div/div/div/button')
        done_button.click()
        save_screenshot(driver, "TravelerDoneClicked")
        logging.info('Passengers set')

        # SEARCH
        search_button = driver.find_element(By.XPATH, '//*[@id="search_button"]')
        search_button.click()
        save_screenshot(driver, "SearchSubmitted")
        logging.info('Search submitted')
        time.sleep(5)

        # FLIGHT PART
        # Wait for flight results to be visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//li[@data-test-id='offer-listing'])[1]"))
        )
        second_item = driver.find_element(By.XPATH, "(//li[@data-test-id='offer-listing'])[1]")
        second_item.click()
        save_screenshot(driver, "FlightSelected")
        logging.info('Flight selected')

    finally:
        # Close the browser
        time.sleep(10)
        logging.info('Ending session')
        driver.quit()