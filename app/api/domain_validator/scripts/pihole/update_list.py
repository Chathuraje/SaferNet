import requests
import json
# from app import settings

import os
from dotenv import load_dotenv
import configparser

load_dotenv()

PIHOLE_API_URL = f"http://pihole.techincog.com/admin/api.php"
PIHOLE_API_KEY = os.getenv("PI_HOLE_API_KEY") 



def __check_domain_status(domain, list_type):
    payload = {
        "auth": PIHOLE_API_KEY,
    }
        
    payload["list"] = list_type
    response = requests.get(PIHOLE_API_URL, params=payload)
    blacklist_domains = json.loads(response.text)["data"]
    
    for item in blacklist_domains:
        if item["domain"] == domain:
            return 1
    
    return 0

def __check_all_the_list(domain):
    list_type = ["white", "black", "regex_white", "regex_black"]
    
    for item in list_type:
        if __check_domain_status(domain, item) == 1:
            return 1, item
    
    return 0, 0


def __add_domain_to_list(domain, list_type):
    payload = {
    "add": domain,
    "list": list_type,
    "auth": PIHOLE_API_KEY,
    }
    response = requests.post(PIHOLE_API_URL, params=payload)
    response_data = json.loads(response.text)["success"]
    
    return response_data
        
    
def add_domain(domain, list_type):
    list_data, _ = __check_all_the_list(domain)
    if list_data == 1:
        return {"success": "False", "message": f"{domain}: Domain already in the list."}

    if __add_domain_to_list(domain, list_type) == True:
        return {"success": "True", "message": f"{domain}: Domain added to {list_type}."}
    else:
        return {"success": "False", "message": f"{domain}: Error adding domain to {list_type}."}
    
    
def view_list(list_type):
    payload = {
        "auth": PIHOLE_API_KEY,
    }
        
    payload["list"] = list_type
    response = requests.get(PIHOLE_API_URL, params=payload)
    domains = json.loads(response.text)["data"]
    
    return domains


def view_complete_list():
    list_type = ["white", "black", "regex_white", "regex_black"]

    complete_list = []
    for item in list_type:
        current_list = view_list(item)
        for entry in current_list:
            domain = entry.get('domain')
            if domain:
                complete_list.append(domain)
    
    return complete_list

def check_domain(url):
    list_data, list_type = __check_all_the_list(url)
    if list_data == 1:
        return list_type
    else:
        return list_type