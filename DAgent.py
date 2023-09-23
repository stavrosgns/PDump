import requests
import os
import json
import csv
import math
import time
import traceback
import sys
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime


class DAgent:
    API_ENDPOINT = "https://api.dehashed.com/search?query="

    def __init__(self):
        """
        | API Limits, Defaults & Behaviour |
        1) Default Results Per Call: 100
        2) Maximum Results Per Call: 10000
        3) Default Record Accessible Via Pagination: 30000
            - That is you can use this kind of combination of &page and &size GET Variables, &size=10000&page=3 that is 30K
            - In other words results are limited to 30000 (30K) results
        4) Rate Limit: 5 requests per second
        5) The API response only to 'application/json' requests
        6) Basic authentication is needed by providing the following information, 'email:API'
        7) Service accepts only 'GET' requests

        | Logic Behind |
        1) self.maxResults = 10000 <=> In order to minimize API Credits consumption, we are setting using the maximum number of results that a call can return
           If we leave the default setting, 100 results per call, and the available results are more than that we will need to perform the request anew
           with setting a greater size capacity. Finally, having set the size=10000 and the available results are 5000, we do not have a problem as we performed
           a single call thus consumed an API Credit
        """
        self.maxResults = 10000
        self.accept_header = 'application/json'

        load_dotenv("./.env") #  Load the environmental variables from the .env file [Create that file manually]
        self.email = os.getenv("EMAIL") #  Change the environment variable with yours, otherwise create such a variable
        self.api = os.getenv("API_KEY") #  Change the environment variable with yours, otherwise create such a variable

        self.__create_results_and_log_folders()

    def __create_results_and_log_folders(self):
        """
        This function will be used in the __init__ when every instance is created
        These two folders are needed in order to save various outputs
          - The API's JSON response is saved in the 'log' folder for redundancy purposes
          - The conversion of JSON => CSV and CSV => XLSX is saved in 'results' folder
        """
        if (not os.path.exists('./log')) and (not os.path.exists('./results')):
            os.mkdir("./log")
            os.mkdir("./results")

    def __write_json_response_to_file(self, data, filename):
        """
        :param data: This is the GET response in json format
        :param filename: a name that should show what kind of information has been stored

        This function writes the response of the JSON to the log folder for redundancy purpose.
        That is, in case that something went wrong with the following processes or another operations
        should be performed on the data, we will not have to request the server again and consume
        API credits
        """
        now = datetime.now()
        current_time = now.strftime("%d%m_%H%M")
        if os.path.exists('./log'):
            with open("./log/" + f"{current_time}-{filename}", "w") as log:
                log.write(data)

        """
        Taking into account how the code is written, there always be the folder 'log'.
        """

    def __convert_json_data_to_csv(self, data, filename):
        """
        :param data: Should be a parsed json response
        :param filename: The filename of the .csv file

        This function takes the parsed JSON object from the API response and
          - Takes the 'entries' key which contains the data (data['entries'])
          - Calculates how many entries there are in the response (size)

        Then trims off the .csv extension of the filename. Do not make a funny face, in line 138, you will observe that
        I am providing the argument filename="<Filename>.csv".

        Having the filename without the extension, I am creating folder to have the result nicely organized into folders
        Then I am just creating the desired file. Let's say we are looking for 'example.com' then I am writing the results
        into file in './results/domain-example.com/domain-example.com.csv'

        The current time is part of the filename in order
        """
        json_entries = data['entries']
        size = len(json_entries)
        print(f"[INFO] {size} were loaded")

        trimmed_filename = os.path.splitext(filename)[0] # => The result would be (filename, .csv) so I care about [0]
        if not os.path.exists(f'./results/{trimmed_filename}'):
            os.mkdir(f'./results/{trimmed_filename}') # Let me satisfy my obsession with cleaning and organize the output by results

        now = datetime.now()
        current_time = now.strftime("%d%m_%H%M")
        with open(f"./results/{trimmed_filename}/{current_time}-{filename}", 'w') as output:
            csv_writer = csv.writer(output)
            count = 0
            for entry in json_entries:
                if count == 0:
                    header = entry.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(entry.values())
        print(f"[INFO] JSON => CSV Completed")

    def __convert_csv_to_xlsx(self, csv, filename, sheetname):
        """
        :param csv: the name of the CSV file that will be loaded
        :param filename: the filename of the XLSX file that we are about to generate
        :param sheetname: The name of the sheet in the XLSX file

        This function takes the csv file that we are going to convert it to a XLSX file.
        The filename parameter contains the filename of the XLSX file, for example test.xlsx
        After applying the os.path.splitext(), trimmed_filename will contain 'test'

        This function is called after the __convert_json_data_to_csv, therefore we know that the
        location './results/{trimmed_filename}/{filename}' exists.
        """
        trimmed_filename = os.path.splitext(filename)[0]

        now = datetime.now()
        current_time = now.strftime("%d%m_%H%M")
        read_csv = pd.read_csv(f"./results/{trimmed_filename}/{current_time}-{csv}")
        excel_writer = pd.ExcelWriter(f"./results/{trimmed_filename}/{current_time}-{filename}")

        read_csv.to_excel(excel_writer,
                          index=False,
                          sheet_name=f"{sheetname}")
        excel_writer._save()
        print("[INFO] CSV => Excel Completed")


    def query_dehashed(self, datatype, data):
        """
        :param datatype: This is could be 'email', 'ip_address', 'username', 'password', 'hashed_password', 'name', 'vin', 'address', 'phone'
        :param data: the value associated with the datatype

        basic_auth: is associated with the 6) under | API Limits, Defaults & Behaviour |
        Successful curl request:
        curl 'https://api.dehashed.com/search?query=username:test' \ <- This should give insights regarding the "custom_url" variable
        -u email@email.com:api-key \
        -H 'Accept: application/json' <- This should give insights regarding the "http_headers" dictionary
        """

        basic_auth = (self.email, self.api)  # auth parameter of the module is accepting tuple
        custom_url = self.API_ENDPOINT + f"{datatype}:{data}" + f"&size={self.maxResults}"
        http_headers = {"Accept": f"{self.accept_header}"}

        try:
            returned_json = requests.get(custom_url, auth=basic_auth, headers=http_headers)
            if returned_json.status_code == 200:
                print(f'[SUCCESS] Data successfully requested and retrieved')
                self.__write_json_response_to_file(returned_json.text,f"{datatype}-{data}.json") # for logging and redundancy purposes
                print(f'[INFO] Response was saved to a log file. Check the \'log\' folder under the filename \'{datatype}-{data}.json')

                parsed_json = json.loads(returned_json.text)
                self.__convert_json_data_to_csv(parsed_json,f"{datatype}-{data}.csv")
                self.__convert_csv_to_xlsx(f"{datatype}-{data}.csv", f"{datatype}-{data}.xlsx", data)

                if parsed_json['total'] > self.maxResults: # will need pagination
                    number_of_pages = math.ceil(parsed_json['total'] / self.maxResults)
                    print(f'[INFO] {number_of_pages} pages of results will be retrieved adhering to rate limits')

                    for page in range(2, number_of_pages):
                        print(f'[INFO] Page {page} - Sleeping for 2 seconds')
                        time.sleep(2)  # stop for a couple of seconds whatever you are trying to do just to be safe with the rate limit

                        results = requests.get(custom_url + f"&page={page}", auth=basic_auth, headers=http_headers)
                        if results.status_code == 200:
                            self.__write_json_response_to_file(results.text, f"{datatype}-{data}-{page}.json")
                            parsed_results = json.loads(results.text)
                            if ('message' in parsed_results.keys()) and ('Bad Size/Page' in parsed_results['message']):
                                print(f"[LIMIT] Hard-Limit reached! Only the first 30K results can be dumped")
                                sys.exit(999)
                            self.__convert_json_data_to_csv(parsed_results, f"{datatype}-{data}-{page}.csv")
                            self.__convert_csv_to_xlsx(f"{datatype}-{data}-{page}.csv", f"{datatype}-{data}-{page}.xlsx", data)
                        else:
                            print(f'[WARNING] Something happened while requesting page {page}')
            elif returned_json.status_code == 401:
                print("[Warning] Invalid API Credentials")
                sys.exit(401)
            elif returned_json.status_code == 400:
                print("[Warning] Too many requests were performed in a small amount of time")
                sys.exit(400)
        except Exception as e:
            print("[EXCEPTION] An exception was occurred while requesting the API endpoint")
            print(f"[STACK TRACE]:\n{traceback.print_exc()}")
            sys.exit(-1)

"""
Exist Codes:
-  -1: Unhandled Exception
- 401: Invalid API Credentials
- 400: Too many requests
- 999: Hard-Limit reached
"""