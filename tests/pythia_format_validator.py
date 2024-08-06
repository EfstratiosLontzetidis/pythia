from termcolor import colored
import re
from datetime import datetime

PYTHIA_VALID_FILTERS = [
    'label', 'ip_address', 'cidr', 'server', 'domain', 'hostname', 'organization',
    'port_number', 'base_protocol', 'protocol', 'port_size_gt', 'port_size_lt', 'port_size',
    'operating_system', 'application', 'product_version', 'product', 'time_scanned',
    'common_platform_enumeration_cpe', 'country_code', 'country_name', 'postal_code', 'state_name',
    'region_name', 'city_name', 'autonomous_system_number', 'autonomous_system_name',
    'autonomous_system_organization', 'http_title', 'http_header_hash', 'http_header',
    'service_banner_hash', 'service_banner', 'http_body_hash', 'http_body', 'http_status_code',
    'http_favicon_hash_dec', 'http_favicon_hash', 'tls_certificate_issuer_org',
    'tls_certificate_subject_org', 'tls_certificate_subject_cn', 'tls_certificate_issuer_cn',
    'tls_certificate_issuer', 'tls_certificate_subject', 'tls_certificate_not_after',
    'tls_certificate_not_before', 'tls_certificate_sha1', 'tls_certificate_sha256',
    'tls_certificate_md5', 'tls_certificate_is_expired', 'tls_certificate.is_valid',
    'tls_certificate.pubkey_rsa_bits', 'tls_certificate_pubkey_ecdsa_bits',
    'tls_certificate_pubkey_type', 'tls_certificate_cipher_name', 'tls_certificate_algorithm',
    'tls_certificate_version', 'tls_certificate', 'jarm_fingerprint', 'ja3s_fingerprint',
    'ja4s_fingerprint', 'ssh_hassh', 'ssh_banner_sha256', 'ssh_banner', 'ssh_key_length',
    'ssh_fingerprint'
]

REQUIRED_FIELDS = {
    'title': str, 'id': str, 'status': str, 'description': str, 'references': list, 'tags': list,
    'author': str, 'date': str, 'query': dict, 'falsepositives': list, 'level': str
}

def validate_fields_exist(rule):
    for field, field_type in REQUIRED_FIELDS.items():
        if field not in rule:
            print(colored("[-]", 'red') + f"Missing field: {field}")
            return False
        if not isinstance(rule[field], field_type):
            print(colored("[-]", 'red') + f"Incorrect type for field: {field}")
            return False
    return True

def validate_non_empty(value, field_name):
    if value:
        return True
    print(colored("[-]", 'red') + f"{field_name} cannot be empty")
    return False

def validate_choice(value, field_name, choices):
    if value in choices:
        return True
    print(colored("[-]", 'red') + f"Invalid {field_name}")
    return False

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y/%m/%d')
        return True
    except ValueError as e:
        print(e)
        return False

def validate_list_elements(lst, field_name):
    if isinstance(lst, list) and all(isinstance(item, str) for item in lst):
        return True
    print(colored("[-]", 'red') + f"Invalid list element in {field_name} section")
    return False

def validate_query(query):
    if 'parameters' not in query or 'condition' not in query:
        print(colored("[-]", 'red') + f"Missing field: {'parameters' if 'parameters' not in query else 'condition'}")
        return False
    if not isinstance(query['parameters'], dict):
        print(colored("[-]", 'red') + "Parameters are not of type dict")
        return False
    if not isinstance(query['condition'], str):
        print(colored("[-]", 'red') + "Condition is not of type string")
        return False
    for conditions in query['parameters'].values():
        if not isinstance(conditions, dict):
            print(colored("[-]", 'red') + "Invalid query format parameters and filters")
            return False
        for key, value in conditions.items():
            if not isinstance(value, str) or key not in PYTHIA_VALID_FILTERS:
                print(colored("[-]", 'red') + f"Field: '{key}' is not applicable to Pythia")
                return False
    return True

def validate_rule(rule):
    if not validate_fields_exist(rule):
        return False
    return (
        validate_non_empty(rule.get('title'), 'Title') and
        validate_choice(rule.get('status'), 'status', ["experimental", "test", "stable"]) and
        validate_non_empty(rule.get('description'), 'Description') and
        validate_list_elements(rule.get('references', []), 'references') and
        validate_list_elements(rule.get('tags', []), 'tags') and
        validate_non_empty(rule.get('author'), 'Authors') and
        validate_date_format(rule.get('date', '')) and
        validate_query(rule.get('query', {})) and
        validate_list_elements(rule.get('falsepositives', []), 'falsepositives') and
        validate_choice(rule.get('level'), 'level', ["low", "moderate", "high"])
    )

def validator(data):
    if validate_rule(data):
        print(colored("[+]", 'green') + data.get('title', '') + "' is valid")
        return True
    else:
        print(colored("[-]", 'red') + data.get('title', '') + " is invalid")
        return False