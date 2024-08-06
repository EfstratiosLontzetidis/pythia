import re
import urllib.parse
import webbrowser
from termcolor import colored
from mappings.pythia_zoomeye import pythia_zoomeye_mappings
from config.api_configs import API_KEYS
from api_searcher.api_searcher import search_zoomeye_api

def remove_spaces_around_plus(string):
    # Check if the string contains " + " and remove surrounding spaces
    return re.sub(r'\s+\+\s+', '+', string)

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

def pythia_to_zoomeye_query(data, api=False, output_file=None, browser=False):
    log_message("Converting to ZOOMEYE format...", output_file)
    condition = data['query']['condition']
    new_condition = condition

    for part in data['query']['parameters']:
        part_number = part
        for key in data['query']['parameters'][part].keys():
            string_part_number = key + data['query']['parameters'][part][key] if pythia_zoomeye_mappings[key] != "" else ""
            new_condition = new_condition.replace(part_number, string_part_number)

    zoomeye_condition = " " + new_condition
    for field, replacement in pythia_zoomeye_mappings.items():
        operator = field
        if field in ["or", "and"]:
            operator = rf'(?<=\s){field}(?=\s)'
        elif field == "*":
            operator = re.escape(field)
        zoomeye_condition = re.sub(operator, replacement, zoomeye_condition)
    zoomeye_condition = limit_spaces(zoomeye_condition[1:])
    zoomeye_condition=remove_spaces_around_plus(zoomeye_condition)

    query_url = "https://www.zoomeye.hk/searchResult?q=" + urllib.parse.quote(zoomeye_condition)
    log_message(f"ZOOMEYE Query: {zoomeye_condition}", output_file, 'green')
    log_message(f"ZOOMEYE Query URL: {query_url}", output_file, 'green')

    if browser:
        webbrowser.open(query_url)

    if api:
        api_key = API_KEYS.get('zoomeye_api_key', '')
        if api_key not in ['', 'changeme']:
            search_zoomeye_api(api_key, urllib.parse.quote(zoomeye_condition), output_file)
        else:
            log_message("Error: API_KEY is not provided for ZOOMEYE API", output_file, 'red')