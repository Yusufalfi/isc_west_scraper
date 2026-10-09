# # graphql_fetcher.py
# import requests
# import time
# import urllib3
# from config import GRAPHQL_URL, GRAPHQL_HEADERS

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# EVENT_EDITION_ID = "eve-656e9625-bc89-4229-a1ee-7c2c8ab7f512"

# def fetch_single_exhibitor_detail(org_id: str) -> dict:
#     # Menggunakan string query persis seperti payload browser asli
#     query_str = f'''{{
#       exhibitingOrganisation(eventEditionId:"{EVENT_EDITION_ID}", organisationId:"{org_id}"){{
#           id  
#           organisationId
#           companyName
#           contactEmail
#           website
#           phone
#           multilingual {{
#            logoUrl
#            displayName
#            description
#            showObjective
#            addressLine1
#            city
#            stateProvince
#            country
#           }}
#           stands{{
#             name
#           }}
#       }}
#     }}'''

#     payload = {"query": query_str}

#     try:
#         res = requests.post(
#             GRAPHQL_URL, 
#             headers=GRAPHQL_HEADERS, 
#             json=payload, 
#             timeout=10, 
#             verify=False
#         )
        
#         if res.status_code == 200:
#             data = res.json().get("data", {})
#             return data.get("exhibitingOrganisation") or {}
#         else:
#             print(f"   ❌ HTTP Error {res.status_code} untuk ID: {org_id}")
            
#     except Exception as e:
#         print(f"   ❌ Error: {e}")
        
#     return {}

# def fetch_details_from_list(exhibitor_list: list, delay=0.2) -> list:
#     raw_results = []
#     total = len(exhibitor_list)
    
#     print(f"🚀 [GraphQL] Mengambil detail untuk {total} exhibitor...")
#     for idx, item in enumerate(exhibitor_list, 1):
#         org_id = item.get("organisationId") or item.get("id")
#         comp_name = item.get("name") or "Unknown"
        
#         print(f"[{idx}/{total}] Fetching: {comp_name} ({org_id})...")
        
#         detail = fetch_single_exhibitor_detail(org_id)
#         if detail:
#             raw_results.append(detail)
#             email = detail.get("contactEmail") or "N/A"
#             print(f"   ✅ Success! Email: {email}")
#         else:
#             print(f"   ⚠️ Gagal ambil data {comp_name}")
            
#         time.sleep(delay)
        
#     return raw_results


# graphql_fetcher.py
import requests
import time
import urllib3
from config import (
    GRAPHQL_URL, 
    GRAPHQL_HEADERS, 
    GRAPHQL_DETAIL_QUERY, 
    EVENT_EDITION_ID
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_single_exhibitor_detail(org_id: str) -> dict:
    """Mengambil detail 1 exhibitor dari GraphQL menggunakan GraphQL Variables."""
    payload = {
        "query": GRAPHQL_DETAIL_QUERY,
        "variables": {
            "eventEditionId": EVENT_EDITION_ID,
            "organisationId": org_id
        }
    }

    try:
        res = requests.post(
            GRAPHQL_URL, 
            headers=GRAPHQL_HEADERS, 
            json=payload, 
            timeout=10, 
            verify=False
        )
        
        if res.status_code == 200:
            data = res.json().get("data", {})
            return data.get("exhibitingOrganisation") or {}
        else:
            print(f"   ❌ HTTP Error {res.status_code} untuk ID: {org_id}")
            
    except Exception as e:
        print(f"   ❌ Exception Error: {e}")
        
    return {}

def fetch_details_from_list(exhibitor_list: list, delay=0.2) -> list:
    """Iterasi list ID dan kumpulkan raw response dari GraphQL."""
    raw_results = []
    total = len(exhibitor_list)
    
    print(f"🚀 [GraphQL] Mengambil detail untuk {total} exhibitor...")
    for idx, item in enumerate(exhibitor_list, 1):
        org_id = item.get("organisationId") or item.get("id")
        comp_name = item.get("name") or "Unknown"
        
        print(f"[{idx}/{total}] Fetching: {comp_name} ({org_id})...")
        
        detail = fetch_single_exhibitor_detail(org_id)
        if detail:
            raw_results.append(detail)
            email = detail.get("contactEmail") or "N/A"
            print(f"   ✅ Success! Email: {email}")
        else:
            print(f"   ⚠️ Gagal ambil data {comp_name}")
            
        time.sleep(delay)
        
    return raw_results