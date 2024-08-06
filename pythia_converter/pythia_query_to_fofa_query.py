import re
import base64
import webbrowser
from termcolor import colored
from mappings.pythia_fofa import pythia_fofa_mappings
from config.api_configs import API_KEYS
from api_searcher.api_searcher import search_fofa_api

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

def pythia_to_fofa_query(data, api=False, output_file=None, browser=False):
    log_message("Converting to FOFA format...", output_file)
    condition = data['query']['condition']
    new_condition = condition

    for part in data['query']['parameters']:
        part_number = part
        for key in data['query']['parameters'][part].keys():
            if pythia_fofa_mappings[key] == "":
                string_part_number = ""
            else:
                string_part_number = key + data['query']['parameters'][part][key]
            new_condition = new_condition.replace(part_number, string_part_number)

    fofa_condition = " " + new_condition
    for field, replacement in pythia_fofa_mappings.items():
        operator = field
        if field in ["or", "and"]:
            operator = rf'(?<=\s){field}(?=\s)'
        elif field == "*":
            operator = re.escape(field)
        fofa_condition = re.sub(operator, replacement, fofa_condition)
    fofa_condition = limit_spaces(fofa_condition[1:])

    fofa_query_url = "https://en.fofa.info/result?qbase64=" + base64.b64encode(fofa_condition.encode('utf-8')).decode('utf-8')
    log_message(f"FOFA Query: {fofa_condition}", output_file, 'green')
    log_message(f"FOFA Query URL: {fofa_query_url}", output_file, 'green')

    if browser:
        webbrowser.open(fofa_query_url)

    if api:
        api_key = API_KEYS.get('fofa_api_key', '')
        if api_key not in ['', 'changeme']:
            search_fofa_api(api_key, base64.b64encode(fofa_condition.encode('utf-8')).decode('utf-8'), output_file)
        else:
            log_message("Error: API_KEY is not provided for FOFA API", output_file, 'red')