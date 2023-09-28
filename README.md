# PDump
![image](https://github.com/stavrosgns/PDump/assets/59849433/e74a884e-f27c-496a-b040-ac669892fbf1)

A Command Line Interface (CLI) tool which harness the power of DEHASHED API to retrieve leaked information for DEHASHED Data Well

# About The Tool
## Insperation
During an assessment, I found myself CURLing the DEHASHED API, redirecting the output to files and then writing a couple of python lines to convert the JSON format to CSV. Doing this process once was fun, but then it was mandane as the searches increased.
That was the epiphany moment of _F**k it! I'll automate this sh*t!_

The idea to convert CSV to XLSX was to include MACROs to get initial access to the client once opened! Nah, I am joking :P

The reason was that brings value to the client and after a couple of tunes using Excel can be considered a deliverable.

## Behavior on the Filesystem
### Output Location
Upon execution of the script two folders are created
- _log_ => Where the JSON response of the API is saved
- _results_ => Where the CSV and XLSX files are saved inside another folder whose name depends on the search type and search data

- [ ] Program the tool to have a fixed location to save the output, otherwise the filesystem will be full of _log_ and _results_ folders

### Output Format
PDump is saving the results in 3 output formats
 - _JSON_ => This is the response of the API and is save with the aim of not comsuming API credits again if you want to perform some other kind of operations on the data
 - _CSV_ => The format was selected for the response to be more human readable
 - _XLSX_ => The tool is using the CSV format to generate a XLSX file using pandas for the ultimate human-friendly representation of the data

### Filename Conventions
The folders in which he output data are saved follow the namespace _{search type}-{search data}-{page}_, if there is a pagination. For example, **domain-gmail.com-1** would be the folder name in case the following command is executed 
```python
python3 pdump domain -s gmail.com
```

The filenames adhere to a different namespace _{currentDaycurrentMonth_currentHourcurrentMinute}-{search type}-{search data}_. For example, **2309_1257-domain-gmail.com.csv** would be the filename in case the following command is executed and the datetime is **23/09/2023 12:57**
```python
python3 pdump domain -s gmail.com
``` 
# Getting Started
## Requirements
For the tool to be functional, the following python3 modules should be installed
```
requests openpyxl pandas python-dotenv
```

This can be done by executing the following command
```
python3 -m pip install -r requirements
```

## Usage

![image](https://github.com/stavrosgns/PDump/assets/59849433/7a528e98-6c33-4df8-a3bc-246ab34858dc)

API provides with the capabilities to search for _domain, email, username, password, hashed_password, vin, phone, name, ip_address_
- The code has been currently tested against **domain, email, username, password**

Therefore, the CLI arguments should be
```python
  python3 pdump.py domain -s gmail.com
  ```
  
```python
  python3 pdump.py password -f passwords.txt
  ```
# Acknowledgements
I want to shout out my gratitude for my colleague and friend [NickVourd](https://github.com/nickvourd) for his ethusiasm and believing that is not just a tool

# License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
