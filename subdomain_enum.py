import requests
import json
from sys import argv
from os import environ
# API Key
API_KEY = environ.get("sectrails_key",None)

def check_key():
    if not API_KEY:
        print("No valid API key")
        exit()

if len(argv) < 2:
    print(f"""USAGE:
          {argv[0]} <domain>""")
    exit()
    
query = f"SELECT domain.hostname FROM hosts WHERE domain.hostname LIKE '%.{argv[1]}'"

def write_results(records):
    filename = f"{argv[1]}.results.txt"
    with open(filename, "a", encoding="utf-8") as output_file:
        for record in records:
            hostname = record["domain"]["hostname"]
            if hostname:
                output_file.write(hostname + "\n")



def first_request():
    check_key()
    print("[+] Sending First Request")
    url = "https://api.securitytrails.com/v1/query/scroll/"
    headers = {
            "APIKEY": API_KEY,
            "Content-Type": "application/json"
    }
    data = {
            "query": query
    }
    response = requests.post(url, json=data, headers=headers)
    total_results = json.loads(response.text)["total"]["value"]
    print(f"Total Results: {total_results}")
    write_results(json.loads(response.text)["records"])
    return json.loads(response.text)["id"]


    

# SQL query

# reverse ip lookup => "SELECT domain.hostname FROM hosts WHERE ip.address='1.1.1.1'"
# subdomains => "SELECT domain.hostname FROM hosts WHERE domain.apex='example.com'"
# conpany domains => "SELECT domain.apex FROM hosts WHERE organization.name='Example Org'"
def fetch():
    check_key()
    scrol_id = first_request()
    num = 2
    while scrol_id:
        url= "https://api.securitytrails.com/v1/query/scroll/" + scrol_id
        print(f"Fetch Request Number: {num}, Send To: {url}")
        headers = {
            "APIKEY": API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        try:
           records = json.loads(response.text)["records"]
           write_results(records)
           scrol_id = json.loads(response.text)["id"]
           num+=1
        except:
            print("[-] Exsit ...")
            print(response.status_code)
            print(response.text)
            exit()

fetch()
