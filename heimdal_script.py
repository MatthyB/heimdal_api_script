import requests
import json
from datetime import datetime, timedelta
import time
import csv
import configparser
import sys

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def main(config_path):
    config = read_config(config_path)

    base_url = config["HeimdalConfig"]["base_url"]
    heimdal_modules_3days = config["HeimdalConfig"]["heimdal_modules_3days"].split(",")
    heimdal_modules_15minutes = config["HeimdalConfig"]["heimdal_modules_15minutes"].split(",")
    heimdal_modules_1hours = config["HeimdalConfig"]["heimdal_modules_1hours"].split(",")
    logstash_url = config["HeimdalConfig"]["logstash_url"]

    customer_group_data = []
    for section in config.sections():
        if section.startswith("CustomerGroupData"):
            customer_info = dict(config[section])
            customer_group_data.append(customer_info)

    current_time = datetime.now()

    next_3days_retrieval = current_time - timedelta(days=3)
    next_15minutes_retrieval = current_time - timedelta(minutes=15)
    next_1hour_retrieval = current_time - timedelta(hours=1)

    while True:
        current_time = datetime.now()

        if current_time >= next_3days_retrieval:
            # ... (hetzelfde als in je oorspronkelijke script)
            for customer_info in customer_group_data:
                customer_id = customer_info["customer_id"]
                bearer_token = customer_info["bearer_token"]
                customer_group = customer_info["customer_group"]

                for heimdal_module in heimdal_modules_3days:
                    # Calculate the start and end dates
                    end_date = current_time.strftime("%Y-%m-%d")
                    start_date = (current_time - timedelta(days=1)).strftime("%Y-%m-%d")

                    # Make the API call
                    url = f"{base_url}{heimdal_module}?customerId={customer_id}&startDate={start_date}&endDate={end_date}"
                    headers = {
                        "Authorization": bearer_token
                    }
                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        # Print the response to the command line
                        print(response.text)

                        # Create the output file for the customer
                        output_file_name = f"heimdal-customer-ids_{customer_group}.csv"

                        # Write the JSON response to a CSV file
                        with open(output_file_name, 'w', newline='') as csv_file:
                            data = response.json()
                            csv_writer = csv.writer(csv_file)
                            # Assuming the JSON response is a list of dictionaries
                            for row in data:
                                if not csv_writer:
                                    # Write the header row using keys from the first dictionary
                                    csv_writer.writerow(row.keys())
                                # Write the data rows
                                csv_writer.writerow(row.values())
                    else:
                        print(f'API call failed with status code: {response.status_code}')

            next_3days_retrieval = current_time + timedelta(days=3)

        if current_time >= next_15minutes_retrieval:
            # ... (hetzelfde als in je oorspronkelijke script)
            for customer_info in customer_group_data:
                bearer_token = customer_info["bearer_token"]
                customer_group = customer_info["customer_group"]

                # Read customer IDs and names from the appropriate CSV file
                csv_filename = f'heimdal-customer-ids_{customer_group}.csv'
                customer_data = []

                with open(csv_filename, 'r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        customer_data.append({
                            "customer_id": row[0],
                            "customer_name": row[1]
                        })

                for customer_info in customer_data:
                    customer_id = customer_info["customer_id"]
                    customer_name = customer_info["customer_name"]

                    for heimdal_module in heimdal_modules_15minutes:
                        # Calculate the start and end dates
                        end_date = current_time.strftime("%Y-%m-%dT%H:%M")
                        start_date = (current_time - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M")

                        # Make the API call
                        url = f"{base_url}{heimdal_module}?customerId={customer_id}&startDate={start_date}&endDate={end_date}"
                        headers = {
                            "Authorization": bearer_token
                        }
                        response = requests.get(url, headers=headers)

                        if response.status_code == 200:
                            data = response.json()

                            # Add the customer name and module as JSON fields
                            for event in data:
                                if isinstance(event, dict):
                                    event["customer_name"] = customer_name
                                    event["heimdal_module"] = heimdal_module

                            # Send the data to Logstash
                            try:
                                response = requests.post(logstash_url, json=data)
                                if response.status_code == 200:
                                    print(f"{current_time}: Data sent to Logstash for customer: {customer_name}, module: {heimdal_module}")
                                else:
                                    print(f"Failed to send data to Logstash for customer: {customer_name}, module: {heimdal_module}, error code: {response.status_code}")
                            except Exception as e:
                                print(f"Error sending data to Logstash: {str(e)}")


            next_15minutes_retrieval = current_time + timedelta(minutes=15)

        if current_time >= next_1hour_retrieval:
            # ... (hetzelfde als in je oorspronkelijke script)
            for customer_info in customer_group_data:
                bearer_token = customer_info["bearer_token"]
                customer_group = customer_info["customer_group"]

                # Read customer IDs and names from the appropriate CSV file
                csv_filename = f'heimdal-customer-ids_{customer_group}.csv'
                customer_data = []

                with open(csv_filename, 'r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        customer_data.append({
                            "customer_id": row[0],
                            "customer_name": row[1]
                        })

                for customer_info in customer_data:
                    customer_id = customer_info["customer_id"]
                    customer_name = customer_info["customer_name"]

                    for heimdal_module in heimdal_modules_1hours:
                        # Calculate the start and end dates
                        end_date = current_time.strftime("%Y-%m-%dT%H:%M")
                        start_date = (current_time - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")

                        # Make the API call
                        url = f"{base_url}{heimdal_module}?customerId={customer_id}&startDate={start_date}&endDate={end_date}"
                        headers = {
                            "Authorization": bearer_token
                        }
                        response = requests.get(url, headers=headers)

                        if response.status_code == 200:
                            data = response.json()

                            # Add the customer name and module as JSON fields
                            for event in data:
                                if isinstance(event, dict):
                                    event["customer_name"] = customer_name
                                    event["heimdal_module"] = heimdal_module

                            # Send the data to Logstash
                            try:
                                response = requests.post(logstash_url, json=data)
                                if response.status_code == 200:
                                    print(f"{current_time}: Data sent to Logstash for customer: {customer_name}, module: {heimdal_module}")
                                else:
                                    print(f"Failed to send data to Logstash for customer: {customer_name}, module: {heimdal_module}, error code: {response.status_code}")
                            except Exception as e:
                                print(f"Error sending data to Logstash: {str(e)}")

            next_1hour_retrieval = current_time + timedelta(hours=1)

        #time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Gebruik: python3 heimdal_script.py config.ini")
        sys.exit(1)

    config_path = sys.argv[1]
    main(config_path)
