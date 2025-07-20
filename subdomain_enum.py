import requests
import sys,json
# API Key
API_KEYS = ["KEY1","KEY2"]

domain = sys.argv[1]
query = f"SELECT domain.hostname FROM hosts WHERE domain.hostname LIKE '%.{domain}'"

def write_results(records):
    filename = f"{domain}.results.txt"
    with open(filename, "a", encoding="utf-8") as output_file:
        for record in records:
            hostname = record["domain"]["hostname"]
            if hostname:
                output_file.write(hostname + "\n")


def get_api_key():
    #print("[+] Gettting a Working API Key")
    for api_key in API_KEYS:
        req = requests.get(f"https://api.securitytrails.com/v1/ping?apikey={api_key}", headers={"Accept":"application/json"})
        if req.status_code == 200:
           return api_key
    print("No Valid API key")
    exit()


def first_request():
    api_key = get_api_key()
    print("[+] Sending First Request")
    url = "https://api.securitytrails.com/v1/query/scroll/"
    headers = {
            "APIKEY": api_key,
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
    scrol_id = first_request()
    num = 2
    while scrol_id:
        api_key = get_api_key()
        url= "https://api.securitytrails.com/v1/query/scroll/" + scrol_id
        print(f"Fetch Request Number: {num}, Send To: {url}")
        headers = {
            "APIKEY": api_key,
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
