import re
import urllib.parse
import webbrowser
from termcolor import colored
from mappings.pythia_hunter import pythia_hunter_mappings
from config.api_configs import API_KEYS
from api_searcher.api_searcher import search_hunter_api

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

def pythia_to_hunter_query(data, api=False, output_file=None, browser=False):
    log_message("Converting to HUNTER format...", output_file)
    condition = data['query']['condition']
    new_condition = condition

    for part in data['query']['parameters']:
        part_number = part
        for key in data['query']['parameters'][part].keys():
            if pythia_hunter_mappings[key] == "":
                string_part_number = ""
            else:
                string_part_number = key + data['query']['parameters'][part][key]
            new_condition = new_condition.replace(part_number, string_part_number)

    hunter_condition = " " + new_condition
    for field, replacement in pythia_hunter_mappings.items():
        operator = field
        if field in ["or", "and"]:
            operator = rf'(?<=\s){field}(?=\s)'
        elif field == "*":
            operator = re.escape(field)
        hunter_condition = re.sub(operator, replacement, hunter_condition)
    hunter_condition = limit_spaces(hunter_condition[1:])

    hunter_query_url = "https://hunter.how/list?searchValue=" + urllib.parse.quote(hunter_condition)
    log_message(f"HUNTER Query: {hunter_condition}", output_file, 'green')
    log_message(f"HUNTER Query URL: {hunter_query_url}", output_file, 'green')

    if browser:
        webbrowser.open(hunter_query_url)

    if api:
        api_key = API_KEYS.get('hunter_api_key', '')
        if api_key not in ['', 'changeme']:
            search_hunter_api(api_key, hunter_condition, output_file)
        else:
            log_message("Error: API_KEY is not provided for HUNTER API", output_file, 'red')