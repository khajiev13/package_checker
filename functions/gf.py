from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.support import expected_conditions as EC


def check_gf(tracking_number, driver, last_website_checked):
    try:
        if last_website_checked != 'GF':
            # Navigate to the webpage
            driver.get('https://www.hzydky.com/mob/track.htm')

        # Find the tracking number input field and submit button
        tracking_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cno'))
        )
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[value="运单查询"]')
            )
        )

        # Fill in the tracking number and submit the form
        tracking_input.send_keys(tracking_number)
        submit_button.click()
        try:
            driver.switch_to.window(driver.window_handles[-1])
            # Try to locate and click the "Send anyway" button by its ID
            proceed_button = proceed_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, 'proceed-button'))
            )
            proceed_button.click()
        except:
            # Handle the case when the button is not found
            print(
                "The 'Send anyway' button is not present on the page. Continuing...")
        # Wait for the table to load
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'oTHtable'))
        )
        # Get the rows of the table
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # Get the second and last rows
        date_shipped = rows[len(
            rows)-1].find_elements(By.TAG_NAME, 'td')[0].text
        date_arrived = rows[1].find_elements(By.TAG_NAME, 'td')[0].text

        # Calculate the difference in days
        date_format = '%Y-%m-%d %H:%M'
        start_date = datetime.datetime.strptime(date_shipped, date_format)
        end_date = datetime.datetime.strptime(date_arrived, date_format)
        days_difference = (end_date - start_date).days
        # Get the status of the package
        status_element = driver.find_element(By.ID, 'HeaderState')
        status = status_element.text.split('：')[1]

        # Return the result
        print(tracking_number, status, days_difference)
        return tracking_number, status, days_difference

    except Exception as e:
        print("Something went wrong in check_gf function", str(e))
