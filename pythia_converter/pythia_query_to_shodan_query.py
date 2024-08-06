import re
import urllib.parse
import webbrowser
from termcolor import colored
from mappings.pythia_shodan import pythia_shodan_mappings
from config.api_configs import API_KEYS
from api_searcher.api_searcher import search_shodan_api

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

def pythia_to_shodan_query(data, api=False, output_file=None, browser=False):
    log_message("Converting to SHODAN format...", output_file)
    condition = data['query']['condition']
    new_condition = condition

    for part in data['query']['parameters']:
        part_number = part
        for key in data['query']['parameters'][part].keys():
            if pythia_shodan_mappings[key] == "":
                string_part_number = ""
            else:
                string_part_number = key + data['query']['parameters'][part][key]
            new_condition = new_condition.replace(part_number, string_part_number)

    shodan_condition = " " + new_condition
    for field, replacement in pythia_shodan_mappings.items():
        operator = field
        if field in ["or", "and"]:
            operator = rf'(?<=\s){field}(?=\s)'
        elif field == "*":
            operator = re.escape(field)
        shodan_condition = re.sub(operator, replacement, shodan_condition)
    shodan_condition = limit_spaces(shodan_condition[1:])

    shodan_query_url = "https://www.shodan.io/search?query=" + urllib.parse.quote(shodan_condition)
    log_message(f"SHODAN Query: {shodan_condition}", output_file, 'green')
    log_message(f"SHODAN Query URL: {shodan_query_url}", output_file, 'green')

    if browser:
        webbrowser.open(shodan_query_url)

    if api:
        api_key = API_KEYS.get('shodan_api_key', '')
        if api_key not in ['', 'changeme']:
            search_shodan_api(api_key, urllib.parse.quote(shodan_condition), output_file)
        else:
            log_message("Error: API_KEY is not provided for SHODAN API", output_file, 'red')