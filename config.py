
# CONFIG.PY - Konfigurasi Utama Scraper ISC West
# 1. ALGOLIA CONFIG (Digunakan untuk mengambil List 813 ID Exhibitor)
# Endpoint API Algolia tempat pencarian data katalog ISC West dilakukan
ALGOLIA_URL = "https://xd0u5m6y4r-dsn.algolia.net/1/indexes/evt-9634c757-4d4a-4720-8a8a-b031184b55aa-index/query"

# Kredensial khusus dari Algolia (lihat pada Network Tab browser saat search)
ALGOLIA_PARAMS = {
    "x-algolia-agent": "Algolia for JavaScript (3.35.1); Browser",
    "x-algolia-application-id": "XD0U5M6Y4R",
    "x-algolia-api-key": "d5cd7d4ec26134ff4a34d736a7f9ad47"
}

# ID unik edisi ISC West yang sedang aktif
EVENT_EDITION_ID = "eve-656e9625-bc89-4229-a1ee-7c2c8ab7f512"

# Filter bawaan Algolia untuk memfilter hanya data 'exhibitor' edisi ISC West
ALGOLIA_BASE_FILTER = f"recordType:exhibitor AND locale:en-us AND eventEditionId:{EVENT_EDITION_ID}"

# 2. GRAPHQL CONFIG (Digunakan untuk mengambil detail informasi perusahaan)
# Endpoint utama GraphQL API milik Reed Expo
GRAPHQL_URL = "https://api.reedexpo.com/graphql/"

# Header Otorisasi Wajib (Kunci penembus HTTP 401 Unauthorized):
# Tanpa 'x-clientid' & 'rx-event-edition-id', server Reed Expo akan menolak request Python.
GRAPHQL_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 Edg/154.0.0.0",
    "Origin": "https://www.discoverisc.com",
    "Referer": "https://www.discoverisc.com/",
    
    # Header identitas aplikasi web ISC West (didapat dari Request Headers browser)
    "x-clientid": "uhQVcmxLwXAjVtVpTvoerERiZSsNz0om",
    "x-correlationid": "70867eaa-dc95-46cb-b6c0-6887fed965cb",
    "rx-event-edition-id": EVENT_EDITION_ID
}


# 3. QUERY GRAPHQL (Struktur data yang diminta dari server Reed Expo)
# Kueri ini membutuhkan 2 variabel wajib ($eventEditionId & $organisationId)
GRAPHQL_DETAIL_QUERY = """
query GetExhibitorDetail($eventEditionId: String!, $organisationId: String!) {
  exhibitingOrganisation(eventEditionId: $eventEditionId, organisationId: $organisationId) {
    id
    organisationId
    companyName
    contactEmail
    website
    phone
    stands {
      name
    }
    socialMedia {
      name
      url
    }
    multilingual {
      displayName
      description
      showObjective        # Field untuk requirement klien: 'Why visit our stand'
      representedBrands {  # Field untuk requirement klien: 'Brands we will feature'
        name
      }
      addressLine1
      city
      stateProvince
      country
    }
    filterCategories {     # Field untuk requirement klien: 'Product Categories'
      responses {
        multilingual {
          name
        }
      }
    }
  }
}
"""