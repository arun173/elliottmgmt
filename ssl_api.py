import os
import socket
import urllib.error
import requests
import yaml
import pandas as pd

""" This code block will read through and input file 
and run the SSL LAB scan against each host from the input file
Input file will have only the domain name or URL address
Script will call the SSLAPI against each of those hosts and 
generate a readable report out to stdout & to a CSV file"""

def ssl_check(domain_name):

    ip_address=socket.gethostbyname(domain_name)
    print(domain_name, ip_address)
    analyze_url = "https://api.ssllabs.com/api/v3/analyze?host="+domain_name+"&fromCache=on"
    api_url = "https://api.ssllabs.com/api/v3/getEndpointData?host="+domain_name+"&s="+str(ip_address)

    try :
        result = requests.get(analyze_url)
        a = result.json()
        response = requests.get(api_url)
        b = response.json()
        data_a = pd.DataFrame(a)
        data_b = pd.DataFrame(b)

        #pd.set_option("max_columns", None, "max_rows", None)
        #pd.set_option("max_rows", None)

        print(data_b)
        report_file="report_" + str(domain_name) + ".csv"
        data_b.to_csv(report_file, index=True)

    except urllib.error.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as err:
        print(f"Exception encountered:{err}")

if __name__ == "__main__":
    file_name = "inventory.txt"

    with open(file_name, mode="r", encoding="utf-8") as inventory_file:
        for line in inventory_file:
            host_name=line.rstrip('\n')
            ssl_check(domain_name=host_name)
