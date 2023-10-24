import pandas as pd
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, send_file, send_from_directory
from time import sleep
from functions.forty_seven import check_forty_seven
from functions.gf import check_gf


op = webdriver.ChromeOptions()  # Uncomment on production
op.add_argument("--headless")  # Uncomment on production
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")  # Uncomment on production
op.add_argument("--disable-gpu")


driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=op)


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
        last_website_checked = None
        for input_data in input_datas:
            while True:
                try:
                    sleep(3)
                    if input_data.startswith('34'):
                        tracking_number, status, days = check_forty_seven(
                            input_data, driver, last_website_checked)
                        data.append((f"{tracking_number} {status}", days))
                    elif input_data.startswith('GF'):
                        tracking_number, status, days = check_gf(
                            input_data, driver, last_website_checked)
                        data.append((f"{tracking_number} {status}", days))
                    break
                except Exception as e:
                    print("Something went wrong: Tracking number: ", input_data)
                    print(driver.session_id)
                    driver.quit()
                    print(e)
            last_website_checked = input_data[:2]

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
