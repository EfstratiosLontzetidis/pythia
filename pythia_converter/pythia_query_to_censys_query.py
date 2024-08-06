import re
import urllib.parse
import webbrowser
from mappings.pythia_censys import pythia_censys_mappings
from config.api_configs import API_KEYS
from api_searcher.api_searcher import search_censys_api
from termcolor import colored

def limit_spaces(string):
    return re.sub(r'\s+', ' ', string)

def write_output_to_file(file, data):
    with open(file, "a") as f:
        f.write(data)

def log_message(message, file=None, color=None):
    if file:
        write_output_to_file(file, message + "\n")
    else:
        if color:
            print(colored(message, color))
        else:
            print(message)

def pythia_to_censys_query(data, api=False, output_file=None, browser=False):
    log_message("Converting to CENSYS format...", output_file)
    condition = data['query']['condition']
    new_condition = condition

    for part in data['query']['parameters']:
        part_number = part
        for key in data['query']['parameters'][part].keys():
            if pythia_censys_mappings[key] == "":
                string_part_number = ""
            else:
                string_part_number = key + data['query']['parameters'][part][key]
            new_condition = new_condition.replace(part_number, string_part_number)

    censys_condition = " " + new_condition
    for field, replacement in pythia_censys_mappings.items():
        operator = field
        if field in ["or", "and"]:
            operator = rf'(?<=\s){field}(?=\s)'
        elif field == "*":
            operator = re.escape(field)
        censys_condition = re.sub(operator, replacement, censys_condition)
    censys_condition = limit_spaces(censys_condition[1:])

    log_message(f"CENSYS Query: {censys_condition}", output_file, 'green')
    censys_query_url = f"https://search.censys.io/search?resource=hosts&sort=RELEVANCE&per_page=25&virtual_hosts=EXCLUDE&q={urllib.parse.quote(censys_condition)}"
    log_message(f"CENSYS Query URL: {censys_query_url}", output_file, 'green')

    if browser:
        webbrowser.open(censys_query_url)

    if api:
        api_id = API_KEYS.get('censys_api_id', '')
        api_secret = API_KEYS.get('censys_api_secret', '')
        if api_id not in ['', 'changeme'] and api_secret not in ['', 'changeme']:
            search_censys_api(api_id, api_secret, urllib.parse.quote(censys_condition), output_file)
        else:
            log_message("Error: API_ID and API_SECRET not provided for CENSYS API", output_file, 'red')