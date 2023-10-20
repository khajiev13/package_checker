from flask import Flask, request, jsonify, send_file, send_from_directory
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
from io import BytesIO
from flask_cors import CORS, cross_origin #For deployment
import os


driver = None
def forty_seven_calculate_diff_days(inp):
    # Convert the date strings to datetime objects
    date_format = '%Y/%m/%d %H:%M:%S'
    start_date = datetime.strptime(inp[0], date_format)
    end_date = datetime.strptime(inp[1], date_format)
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
            EC.presence_of_element_located((By.XPATH, f'//tr[@data-index="{index_num}"]'))
        )
        # Wait for the <div> element within the <td> to be present
        date_element = WebDriverWait(tr_element, 10).until(
            EC.presence_of_element_located((By.XPATH, './td/div[@class="layui-table-cell laytable-cell-1-0-0"]'))
        )
        date_text = date_element.text
        return date_text
    except Exception as e:
        print("An error occurred:", str(e))
def forty_seven_find(tracking_number):
    try:
        # Wait for the textarea element to be present
        textarea = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.NAME, 'desc'))
        )
        textarea.clear()
        textarea.send_keys(tracking_number)
        # Wait for the button element to be clickable
        button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.ID, 'QueryData'))
        )
        button.click()
        element = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CLASS_NAME, "layui-table-cell"))
        )
        # Wait for the element to be visible
        ID_status = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'layui-table-tool-temp'))
        ).text
        arrived_date = forty_seven_get_date_by_index(0)
        #GEt the last date
        try:
            # Use WebDriverWait to wait for elements with 'data-index' to be present
            elements_with_data_index = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-index]'))
            )

            # Extract and store the 'data-index' values as integers
            data_indices = [int(element.get_attribute('data-index')) for element in elements_with_data_index]

            # Find the maximum 'data-index' value
            max_data_index = max(data_indices)
            last_element = forty_seven_get_date_by_index(max_data_index)
            driver.refresh()
            return last_element,arrived_date, ID_status

        except Exception as e:
            print("An error occurred:", str(e))

    except:
        print("Something went wrong!")
        driver.quit()


def check_forty_seven(tracking_num):
    # Initialize the Chrome WebDriver
    # driver = webdriver.Chrome(executable_path=webdriver_path)
    
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-sh-usage")
    global driver
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=op)
    # Navigate to the webpage
    driver.get('http://47.101.70.255:81/#site9')  # Replace with the actual URL
    # tracking_numbers = [
    # "34Q7P509315401000930807",
    # "34Q7P509315301000930800",
    # "34Q7P509315201000930803",
    # "34Q7P509315101000930806",
    # "34Q7P509315001000930809"
    # ]
    tracking_numbers = tracking_num.split()
    # Define a list to store the data
    data = []
    for tracking_number in tracking_numbers:
        output = forty_seven_find(tracking_number)
        output = forty_seven_calculate_diff_days(output)
        # Split the output into two columns
        tracking_num,status, days = output.rsplit(' ')
        # Append the data as a tuple
        data.append((f"{tracking_number} {status}", days))
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Tracking number', 'Delivered in days'])
    # Save the DataFrame to an Excel file
    # Return a BytesIO object instead of saving the DataFrame to a file
    output_data = BytesIO()
    df.to_excel(output_data, index=False)
    output_data.seek(0)  # Reset the pointer to the beginning of the BytesIO object
    driver.quit()
    return output_data
    


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
@app.route('/check', methods=['POST'])
@cross_origin()
def check_data():
    if request.method == 'POST':
        # Get the data from the request body
        data = request.get_json()

        # Example: Access the 'input' field from the JSON data
        input_data = data.get('input')

        output_data = check_forty_seven(input_data)
        return send_file(
            output_data,
            as_attachment=True,
            download_name='output.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
@app.route('/', methods=['GET'])
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
