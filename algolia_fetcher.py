# algolia_fetcher.py
import requests
import urllib3
from config import ALGOLIA_URL, ALGOLIA_PARAMS, ALGOLIA_BASE_FILTER

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_all_exhibitor_ids(hits_per_page=100):
    all_exhibitors = [] 
    
    first_payload = {
        "params": f"query=&page=0&hitsPerPage={hits_per_page}&filters={ALGOLIA_BASE_FILTER}"
    }
    
    response = requests.post(ALGOLIA_URL, params=ALGOLIA_PARAMS, json=first_payload, verify=False)
    if response.status_code != 200:
        return []
        
    data = response.json()
    total_pages = data.get("nbPages", 0)
    
    for page in range(total_pages):
        payload = {
            "params": f"query=&page={page}&hitsPerPage={hits_per_page}&filters={ALGOLIA_BASE_FILTER}"
        }
        r = requests.post(ALGOLIA_URL, params=ALGOLIA_PARAMS, json=payload, verify=False)
        if r.status_code == 200:
            hits = r.json().get("hits", [])
            for item in hits:
                # Ambil organisationId (org-...) dan id (exh-...)
                exhibitor_id = item.get("id") or item.get("objectID")
                org_id = item.get("organisationId") or item.get("organisationGuid")
                company_name = item.get("displayName") or item.get("name")
                
                # Jika organisationId tidak ada di root, ubah prefix exh- ke org-
                if not org_id and exhibitor_id and exhibitor_id.startswith("exh-"):
                    org_id = exhibitor_id.replace("exh-", "org-")
                elif not org_id:
                    org_id = exhibitor_id

                all_exhibitors.append({
                    "id": exhibitor_id,
                    "organisationId": org_id,
                    "name": company_name
                })
                
    return all_exhibitors