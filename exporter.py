import pandas as pd

def parse_graphql_data(raw_details: list) -> list:
    """Mengubah data GraphQL sesuai kriteria dan urutan kolom spesifik permintaan klien."""
    cleaned_data = []
    
    for item in raw_details:
        multilingual = item.get("multilingual", [])
        ml_info = multilingual[0] if multilingual else {}
        
        # 1. Stand # / Booth Number
        stands = item.get("stands", [])
        stand_numbers = ", ".join([s.get("name", "") for s in stands if s.get("name")])
        
        # 2. LinkedIn Company URL Khusus (Filter hanya LINKEDIN)
        socials = item.get("socialMedia", [])
        linkedin_url = ""
        for soc in socials:
            if soc.get("name", "").upper() == "LINKEDIN":
                linkedin_url = soc.get("url", "")
                break
                
        # 3. Brands We Will Feature
        brands = ml_info.get("representedBrands", [])
        brand_names = ", ".join([b.get("name", "") for b in brands if b.get("name")])
        
        # 4. Product Categories (Comma-separated)
        categories = []
        for cat in item.get("filterCategories", []):
            for resp in cat.get("responses", []):
                for ml in resp.get("multilingual", []):
                    if ml.get("name"):
                        categories.append(ml.get("name"))
        cat_str = ", ".join(list(set(categories)))
        
        # 5. Source URL (URL halaman detail perusahaan)
        org_id = item.get("organisationId", "")
        source_url = f"https://www.discoverisc.com/en-us/exhibitor-details.{org_id}.html" if org_id else ""

        # Menyusun dictionary sesuai urutan 1-9 permintaan klien
        cleaned_data.append({
            "Company Name": item.get("companyName") or ml_info.get("displayName", ""),
            "Website": item.get("website", ""),
            "Email": item.get("contactEmail", ""),
            "Stand #": stand_numbers,
            "LinkedIn Company URL": linkedin_url,
            "Why Visit Our Stand": ml_info.get("showObjective", ""),
            "Description": ml_info.get("description", ""),
            "Brands We Will Feature": brand_names,
            "Product Categories": cat_str,
            "Source URL": source_url
        })
        
    return cleaned_data

def save_to_excel_and_csv(raw_details: list, filename_prefix="isc_west_exhibitors"):
    """Simpan hasil parse ke Excel dan CSV."""
    parsed_data = parse_graphql_data(raw_details)
    df = pd.DataFrame(parsed_data)
    
    excel_file = f"{filename_prefix}.xlsx"
    csv_file = f"{filename_prefix}.csv"
    
    df.to_excel(excel_file, index=False)
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    
    print("\n" + "=" * 60)
    print("💾 DATA HASIL FITUR SESUAI REQUEST KLIEN BERHASIL DISIMPAN!")
    print(f"   📁 File Excel : {excel_file}")
    print(f"   📁 File CSV   : {csv_file}")
    print("=" * 60)