from DAgent import DAgent
import argparse

def signature():
    print()
    print("██████╗ ██████╗ ██╗   ██╗███╗   ███╗██████╗")
    print("██╔══██╗██╔══██╗██║   ██║████╗ ████║██╔══██╗")
    print("██████╔╝██║  ██║██║   ██║██╔████╔██║██████╔╝")
    print("██╔═══╝ ██║  ██║██║   ██║██║╚██╔╝██║██╔═══╝")
    print("██║     ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║")
    print("╚═╝     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝")
    print("A DEHASHED password dumper written by purpl3ph03n1x")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Querying DEHASHED For Leaked Credentials")
    parser.add_argument("query_type", help="domain, email, username, password, vin, phone, name, ip_address, hashed_password")
    parser.add_argument("-s", "--search", help="The value to be searched against DEHASHED database")
    parser.add_argument("-f", '--file', help="A file with New Line Separated values ")
    args = parser.parse_args()

    signature()

    dagent = DAgent() # DEHASHED Agent
    if (args.search is not None) and (args.file is None):
        dagent.query_dehashed(datatype=args.query_type, data=args.search)
    elif (args.search is None) and (args.file is not None):
        with open(args.file, 'r') as qData:
            for entry in qData.readlines():
                dagent.query_dehashed(datatype=args.query_type, data=entry)
    else:
        print(f"[WARNING] You have to provide either a file or a search value")
