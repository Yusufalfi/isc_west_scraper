from algolia_fetcher import get_all_exhibitor_ids
from graphql_fetcher import fetch_details_from_list
from exporter import save_to_excel_and_csv

def run():
    print(" PIPELINE SCRAPER ISC WEST (150 DATA SAMPLE) ===\n")
    
    # 1. get All ID From Algolia
    all_exhibitors = get_all_exhibitor_ids()
    print(f"\n Total ID From Algolia: {len(all_exhibitors)}")
    
    if not all_exhibitors:
        print(" Fail Get ID From Algolia.")
        return

    # 2. Ambil HANYA 150 data pertama
    sample_150 = all_exhibitors[:150]
    print(f"\n for sample get 150 data First.")

    # 3. call detail GraphQL with delay 0.1s
    raw_details = fetch_details_from_list(sample_150, delay=0.1)
    
    # 4. Parse dan save To Excel/CSV
    save_to_excel_and_csv(raw_details)

if __name__ == "__main__":
    run()