import datetime
import pandas as pd
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, send_file, send_from_directory


op = webdriver.ChromeOptions()  # Uncomment on production
op.add_argument("--headless")  # Uncomment on production
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")  # Uncomment on production
op.add_argument("--disable-gpu")
# Add options to ignore certificate errors and insecure certificate warnings
op.add_argument("--ignore-certificate-errors")
op.add_argument("--allow-running-insecure-content")


driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=op)


def check_forty_seven(tracking_number):
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
            # Navigate to the webpage
            # Replace with the actual URL
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


def check_gf(tracking_number):
    try:
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
        for i in range(2):
            try:
                driver.switch_to.window(driver.window_handles[-1])
                # Try to locate and click the "Send anyway" button by its ID
                proceed_button = proceed_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'proceed-button'))
                )
                proceed_button.click()
            except Exception as e:
                print(e)
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
        print(date_shipped, date_arrived)

        # Calculate the difference in days
        date_format = '%Y-%m-%d %H:%M'
        start_date = datetime.datetime.strptime(date_shipped, date_format)
        end_date = datetime.datetime.strptime(date_arrived, date_format)
        days_difference = (end_date - start_date).days
        print(days_difference)
        # Get the status of the package
        status_element = driver.find_element(By.ID, 'HeaderState')
        status = status_element.text.split('：')[1]

        # Return the result
        print(tracking_number, status, days_difference)
        return tracking_number, status, days_difference

    except Exception as e:
        print("An error occurred:", str(e))
        driver.quit()


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/check', methods=['POST'])
@cross_origin()
def check_data():
    if request.method == 'POST':
        # Get the data from the request body
        data = request.get_json()

        # Example: Access the 'input' field from the JSON data and make a list of the input data
        input_datas = data.get('input').split()

        # Define a list to store the data
        data = []
        for input_data in input_datas:
            if input_data.startswith('34'):
                tracking_number, status, days = check_forty_seven(input_data)
                data.append((f"{tracking_number} {status}", days))
            elif input_data.startswith('GF'):
                tracking_number, status, days = check_gf(input_data)
                data.append((f"{tracking_number} {status}", days))

        # Create a DataFrame
        df = pd.DataFrame(
            data, columns=['Tracking number', 'Delivered in days'])

        # Save the DataFrame to an Excel file
        output_data = BytesIO()
        df.to_excel(output_data, index=False)
        output_data.seek(0)
        driver.quit()
        return send_file(
            output_data,
            as_attachment=True,
            download_name='output.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


if __name__ == '__main__':
    app.run(debug=True)
