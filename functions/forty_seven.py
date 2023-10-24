from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.support import expected_conditions as EC


def check_forty_seven(tracking_number, driver, last_website_checked):
    def forty_seven_calculate_diff_days(inp):
        # Convert the date strings to datetime objects
        date_format = '%Y/%m/%d %H:%M:%S'
        start_date = datetime.datetime.strptime(inp[0], date_format)
        end_date = datetime.datetime.strptime(inp[1], date_format)
        # Calculate the difference in days
        days_difference = (end_date - start_date).days
        # Create the new string
        new_string = f"{inp[2]} {days_difference}"
        # Print the new string
        return new_string

    def forty_seven_get_date_by_index(index_num):
        try:
            # Wait for the specific <tr> element with data-index="0" and extract the date
            tr_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//tr[@data-index="{index_num}"]')
                )
            )
            # Wait for the <div> element within the <td> to be present
            date_element = WebDriverWait(tr_element, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     './td/div[@class="layui-table-cell laytable-cell-1-0-0"]')
                )
            )
            date_text = date_element.text
            return date_text
        except Exception as e:
            print("An error occurred:", str(e))
            driver.quit()

    def forty_seven_find(tracking_number):
        try:
            if last_website_checked != '34':
                # Navigate to the webpage
                driver.get('http://47.101.70.255:81/')

            # Wait for the textarea element to be present
            textarea = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.NAME, 'desc'))
            )
            textarea.clear()
            textarea.send_keys(tracking_number)
            # Wait for the button element to be clickable
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'QueryData'))
            )
            button.click()
            element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "layui-table-cell")
                )
            )
            # Wait for the element to be visible
            ID_status = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'layui-table-tool-temp')
                )
            ).text
            arrived_date = forty_seven_get_date_by_index(0)
            # Get the last date
            try:
                # Use WebDriverWait to wait for elements with 'data-index' to be present
                elements_with_data_index = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-index]')
                    )
                )

                # Extract and store the 'data-index' values as integers
                data_indices = [int(element.get_attribute('data-index'))
                                for element in elements_with_data_index]

                # Find the maximum 'data-index' value
                max_data_index = max(data_indices)
                last_element = forty_seven_get_date_by_index(max_data_index)
                driver.refresh()
                return last_element, arrived_date, ID_status

            except Exception as e:
                print("An error occurred:", str(e))

        except Exception as e:
            print("Something went wrong:", str(e))
            driver.quit()

    output = forty_seven_find(tracking_number)
    print(output)
    output = forty_seven_calculate_diff_days(output)
    # Split the output into two columns
    tracking_num, status, days = output.rsplit(' ')

    return tracking_num, status, days
