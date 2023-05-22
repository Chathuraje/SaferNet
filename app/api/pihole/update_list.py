import requests
import json
from app import settings

def __check_domain_status(domain, list_type):
    payload = {
        "auth": settings.PIHOLE_API_KEY,
    }
        
    payload["list"] = list_type
    response = requests.get(settings.PIHOLE_API_URL, params=payload)
    blacklist_domains = json.loads(response.text)["data"]
    
    for item in blacklist_domains:
        if item["domain"] == domain:
            return 1
    
    return 0


def __add_domain_to_list(domain, list_type):
    payload = {
    "add": domain,
    "list": list_type,
    "auth": settings.PIHOLE_API_KEY,
    }
    response = requests.post(settings.PIHOLE_API_URL, params=payload)
    response_data = json.loads(response.text)["success"]
    
    return response_data
        
    
def add_domain(domain, list_type):
    if __check_domain_status(domain, list_type) == 1:
        return {"success": "False", "message": f"{domain}: Domain already in the list."}

    if __add_domain_to_list(domain, list_type) == True:
        return {"success": "True", "message": f"{domain}: Domain added to {list_type}."}
    else:
        return {"success": "False", "message": f"{domain}: Error adding domain to {list_type}."}
    
    
def view_list(list_type):
    payload = {
        "auth": settings.PIHOLE_API_KEY,
    }
        
    payload["list"] = list_type
    response = requests.get(settings.PIHOLE_API_URL, params=payload)
    domains = json.loads(response.text)["data"]
    
    return domains