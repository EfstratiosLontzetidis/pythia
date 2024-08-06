import yaml
import argparse
from argparse import RawDescriptionHelpFormatter
import tests.pythia_format_validator
import pythia_converter
from pythia_converter import (
    pythia_query_to_fofa_query,
    pythia_query_to_full_query,
    pythia_query_to_hunter_query,
    pythia_query_to_censys_query,
    pythia_query_to_shodan_query,
    pythia_query_to_binaryedge_query,
    pythia_query_to_zoomeye_query
)
from api_searcher.api_searcher import *
from termcolor import colored
from pyfiglet import Figlet


def write_output_to_file(file, data):
    with open(file, "a") as f:
        f.write(data)


def load_rule_from_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def validate_rule(data):
    tests.pythia_format_validator.validator(data)


def convert_to_platform_query(data, platform, api, output_file, browser):
    if tests.pythia_format_validator.validator(data):
        print(colored("[!]", 'white') + " Starting Pythia conversion...")
        pythia_converter.pythia_query_to_full_query.pythia_query_parser(data, output_file)
        converters = {
            "FOFA": pythia_converter.pythia_query_to_fofa_query.pythia_to_fofa_query,
            "HUNTER": pythia_converter.pythia_query_to_hunter_query.pythia_to_hunter_query,
            "CENSYS": pythia_converter.pythia_query_to_censys_query.pythia_to_censys_query,
            "SHODAN": pythia_converter.pythia_query_to_shodan_query.pythia_to_shodan_query,
            "ZOOMEYE": pythia_converter.pythia_query_to_zoomeye_query.pythia_to_zoomeye_query,
            "BINARYEDGE": pythia_converter.pythia_query_to_binaryedge_query.pythia_to_binaryedge_query
        }
        converters[platform](data, api, output_file, browser)


def main():
    ascii_art = Figlet(font='big')
    print(colored(ascii_art.renderText('Pythia'), 'white'))
    print("Pythia - Generic Query Format for Discovering Malicious Infrastructure\n")

    parser = argparse.ArgumentParser(
        prog="pythia.py",
        description="",
        epilog="Made by Efstratios Lontzetidis, @lontze7",
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument('-file', required=True, help='Path to the Pythia query YAML file')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-validate', action='store_true', help='Validate the Pythia query format of the file')
    group.add_argument(
        '-convert',
        nargs='+',
        choices=['FOFA', 'CENSYS', 'SHODAN', 'BINARYEDGE', 'ZOOMEYE', 'HUNTER', 'ALL'],
        help='Convert the query to a specified platform format. Separate the platforms using space characters.'
    )
    parser.add_argument('-open_url', action='store_true', help='Open the URLs in a browser. (requires -convert argument)')
    parser.add_argument('-api', action='store_true', help='Search Pythia query results to APIs')
    parser.add_argument('-output_file', help='Output file to store the results')

    args = parser.parse_args()

    print("Initializing Pythia...")
    data = load_rule_from_yaml(args.file)
    if args.validate:
        validate_rule(data)
    elif args.convert:
        platforms = args.convert if 'ALL' not in args.convert else [
            'FOFA', 'CENSYS', 'SHODAN', 'BINARYEDGE', 'ZOOMEYE', 'HUNTER']
        browser = args.open_url
        for platform in platforms:
            print(colored("[!]", 'white') + f" Starting Pythia conversion to {platform} format...")
            if args.output_file:
                write_output_to_file(args.output_file, f"Pythia query to be converted in {platform} format.\n")
            else:
                print(f"Pythia query to be converted in {platform} format.")
            convert_to_platform_query(data, platform, args.api, args.output_file, browser)
            if args.output_file:
                write_output_to_file(args.output_file, "-----------------------------------------------------------------------\n")
            else:
                print("-----------------------------------------------------------------------")
        print(colored("[+]", 'green') + " Pythia conversions run successfully.")


if __name__ == "__main__":
    main()