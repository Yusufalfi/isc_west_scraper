# ALGOLIA CONFIG 
ALGOLIA_URL = "https://xd0u5m6y4r-dsn.algolia.net/1/indexes/evt-9634c757-4d4a-4720-8a8a-b031184b55aa-index/query"

#Query Parameters (Kredensial Otorisasi Algolia)
# Algolia butuhkan 3 params ini di URL/Headers 
# agar mau request (bisa di lihat di header fetch/xhr):
ALGOLIA_PARAMS = {
    "x-algolia-agent": "Algolia for JavaScript (3.35.1); Browser",
    "x-algolia-application-id": "XD0U5M6Y4R",
    "x-algolia-api-key": "d5cd7d4ec26134ff4a34d736a7f9ad47"
}

EVENT_EDITION_ID = "eve-656e9625-bc89-4229-a1ee-7c2c8ab7f512"
ALGOLIA_BASE_FILTER = f"recordType:exhibitor AND locale:en-us AND eventEditionId:{EVENT_EDITION_ID}"

# GRAPHQL CONFIG
GRAPHQL_URL = "https://api.reedexpo.com/graphql/"

GRAPHQL_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 Edg/154.0.0.0",
    "Origin": "https://www.discoverisc.com",
    "Referer": "https://www.discoverisc.com/",
    "x-clientid": "uhQVcmxLwXAjVtVpTvoerERiZSsNz0om",
    "x-correlationid": "70867eaa-dc95-46cb-b6c0-6887fed965cb",
    "rx-event-edition-id": EVENT_EDITION_ID
}

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
      showObjective
      addressLine1
      city
      stateProvince
      country
    }
    filterCategories {
      responses {
        multilingual {
          name
        }
      }
    }
  }
}
"""