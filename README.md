![image](https://github.com/stavrosgns/PDump/assets/59849433/e74a884e-f27c-496a-b040-ac669892fbf1)

                                            

# Description
_PDump_ is a command line inteface (CLI) tool which utilizes the DEHASHED API capabilities to retrieve leaked information from **DEHASHED**

# Output
PDump is saving the results in 3 output formats
 - _JSON_ => This is the response of the API and is save with the aim of not comsuming API credits again if you want to perform some other kind of operations on the data
 - _CSV_ => The format was selected for the response to be more human readable
 - _XLSX_ => The tool is using the CSV format to generate a XLSX file using pandas for the ultimate human-friendly representation of the data

# Usage

![image](https://github.com/stavrosgns/PDump/assets/59849433/7a528e98-6c33-4df8-a3bc-246ab34858dc)

API provides with the capabilities to search for _domain, email, username, password, hashed_password, vin, phone, name, ip_address_
- The code has been currently tested against **domain, email, username, password**

Therefore, the CLI arguments should be
- ```python
  python3 pdump.py <type> -s <search value>
  ``` == For Example ==> python3 pdump.py domain -s gmail.com
- ```python
  python3 pdump.py <type> -f <file of multiple value separated by new line> 
  ``` == For Example ==> python3 pdump.py password -f passwords.txt

# Filename Conventions
The folders in which he output data are saved follow the namespace _{search type}-{search data}-{page}_, if there is a pagination. For example, **domain-gmail.com-1** would be the folder name in case ```python 
python3 pdump domain -s gmail.com
``` command is executed

The filenames adhere to a different namespace _{currentDaycurrentMonth_currentHourcurrentMinute}-{search type}-{search data}_. For example, **2309_1257-domain-gmail.com.csv** would be the filename in case ```python
python3 pdump domain -s gmail.com
``` command is executed and the datetime is 23/09/2023 12:57
