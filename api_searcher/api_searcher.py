import base64
import requests
import ipaddress
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil.relativedelta import relativedelta
from termcolor import colored

def write_output_to_file(file, data):
    with open(file, "a") as f:
        f.write(data)

def is_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def log_message(message, file=None, color=None):
    if file:
        write_output_to_file(file, message + "\n")
    else:
        if color:
            print(colored(message, color))
        else:
            print(message)

def log_api_results(api_name, results, file):
    if results:
        message = f"{api_name} API results were identified"
        log_message(message, file, 'green')
        log_message(json.dumps(results, indent=4), file)
    else:
        message = f"No {api_name} API results identified for this query"
        log_message(message, file, 'red')
    log_message("-----------------------------------------------------------------------", file)

def search_fofa_api(api_key, query, file=None):
    fofa_url = 'https://fofa.info/api/v1/search/all'
    log_message("Starting to search FOFA API...", file)
    response = requests.get(f"{fofa_url}?&key={api_key}&qbase64={query}").json()

    if response.get('error') != 'false':
        log_message(f"Error in FOFA API results: {response.get('errmsg')}", file, 'red')
    else:
        log_api_results("FOFA", response.get('results'), file)

def search_shodan_api(api_key, query, file=None):
    shodan_url = 'https://api.shodan.io/shodan/host/search'
    log_message("Starting to search SHODAN API...", file)
    response = requests.get(f"{shodan_url}?key={api_key}&query={query}").json()

    if response.get('error'):
        log_message(f"Error in SHODAN API results: {response.get('error')}", file, 'red')
    else:
        log_api_results("SHODAN", response.get('matches'), file)

def search_censys_api(api_id, api_secret, query, file=None):
    censys_url = "https://search.censys.io/api/v2/hosts/search"
    log_message("Starting to search CENSYS API...", file)
    response = requests.get(f"{censys_url}?q={query}", auth=HTTPBasicAuth(api_id, api_secret)).json()

    if response['result']['hits']:
        log_api_results("CENSYS", response['result']['hits'], file)
    else:
        log_message(f"No CENSYS API results identified for this query: {query}", file, 'red')

def search_hunter_api(api_key, query, file=None):
    end_time = datetime.now().strftime("%Y-%m-%d")
    start_time = (datetime.now() - relativedelta(months=6)).strftime("%Y-%m-%d")
    hunter_url = 'https://api.hunter.how/search'
    encoded_query = base64.urlsafe_b64encode(query.encode("utf-8")).decode('ascii')
    log_message("Starting to search HUNTER API...", file)
    response = requests.get(
        f"{hunter_url}?api-key={api_key}&query={encoded_query}&start_time={start_time}&end_time={end_time}"
    ).json()

    if response.get('code') not in [200]:
        log_message(f"Error in HUNTER API results for query: {query}", file, 'red')
        log_message(json.dumps(response), file)
    elif response.get('message') == "There were no results matching the query":
        log_message(f"No HUNTER API results identified for this query: {query}", file, 'red')
    else:
        log_api_results("HUNTER", response, file)

def search_zoomeye_api(api_key, query, file=None):
    headers = {
        "API-KEY": api_key,
        "User-Agent": "Pythia 1.0"
    }
    zoomeye_url = 'https://api.zoomeye.hk/host/search'
    log_message("Starting to search ZOOMEYE API...", file)
    response = requests.get(f"{zoomeye_url}?query={query}", headers=headers)

    if response.status_code != 200:
        log_message(f"Error in ZOOMEYE API results for query: {query}", file, 'red')
        log_message(response.content.decode(), file)
    else:
        results = response.json()
        log_api_results("ZOOMEYE", results if results.get('available') else [], file)

def search_binaryedge_api(api_key, query, file=None):
    headers = {"X-Key": api_key}
    binaryedge_url = "https://api.binaryedge.io/v2/query/search"
    log_message("Starting to search BINARYEDGE API...", file)
    response = requests.get(f"{binaryedge_url}?query={query}", headers=headers)

    if response.status_code != 200:
        log_message(f"Error in BINARYEDGE API results for query: {query}", file, 'red')
        log_message(response.content.decode(), file)
    else:
        results = response.json()
        log_api_results("BINARYEDGE", results.get('events'), file)