import re
import urllib.parse
import webbrowser
from mappings.pythia_binaryedge import pythia_binaryedge_mappings
from config.api_configs import API_KEYS
from termcolor import colored
from api_searcher.api_searcher import search_binaryedge_api

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

def pythia_to_binaryedge_query(data, api=False, output_file=None, browser=False):
    log_message("Converting to BINARYEDGE format...", output_file)
    condition = data['query']['condition']
    new_condition = condition

    for part in data['query']['parameters']:
        part_number = part
        for key in data['query']['parameters'][part].keys():
            if pythia_binaryedge_mappings[key] == "":
                string_part_number = ""
            else:
                string_part_number = key + data['query']['parameters'][part][key]
            new_condition = new_condition.replace(part_number, string_part_number)

    binaryedge_condition = " " + new_condition
    for field, replacement in pythia_binaryedge_mappings.items():
        operator = field
        if field in ["or", "and"]:
            operator = rf'(?<=\s){field}(?=\s)'
        elif field == "*":
            operator = re.escape(field)
        binaryedge_condition = re.sub(operator, replacement, binaryedge_condition)
    binaryedge_condition = limit_spaces(binaryedge_condition[1:])

    log_message(f"BINARYEDGE Query: {binaryedge_condition}", output_file, 'green')
    binaryedge_query_url = f"https://app.binaryedge.io/services/query?query={urllib.parse.quote(binaryedge_condition)}"
    log_message(f"BINARYEDGE Query URL: {binaryedge_query_url}", output_file, 'green')

    if browser:
        webbrowser.open(binaryedge_query_url)

    if api:
        api_key = API_KEYS.get('binaryedge_api_key', '')
        if api_key and api_key != 'changeme':
            search_binaryedge_api(api_key, urllib.parse.quote(binaryedge_condition), output_file)
        else:
            log_message("Error: API_KEY not provided for BINARYEDGE API", output_file, 'red')