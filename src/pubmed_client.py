import requests
import time

EMAIL = "avinashmatadeen2@gmail.com"

def search_pubmed(query, max_results=50):
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed", #search pubmed database
        "term": query,  #disease to search for
        "retmax": max_results, #max number of results
        "retmode": "json", #get results in json format
        "email": EMAIL #identity
    }

    #send request to pubmed
    response = rate_limited_request(url, params)

    # Convert the JSON response into a Python dictionary
    data = response.json()

    # Extract the list of PubMed IDs from the response
    pmid_list = data["esearchresult"]["idlist"]
    
    # Return the list
    return pmid_list

# Test the function (only runs when you execute this file directly)
if __name__ == "__main__":
    results = search_pubmed("breast cancer", 5)
    print("PubMed IDs found:", results)

def fetch_article_details(pmid):
    """Fetch title, abstract, and year for a given PubMed ID"""

    # The URL for fetching article summaries
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
     # Parameters for the request
    params = {
        "db": "pubmed",
        "id": pmid,               # The PubMed ID
        "retmode": "json",        # Get JSON format
        "email": EMAIL
    }

    # Send the request
    response = rate_limited_request(url, params)
    data = response.json()
    # Get the article data from the response
    # The response structure: data["result"][pmid] contains the article
    article_data = data["result"][pmid]

    # Create a dictionary with the information we want
    result = {
        "title": article_data.get("title", "No title available"),
        "pubdate": article_data.get("pubdate", "Unknown date"),
        "source": article_data.get("source", "Unknown journal"),
        "pmid": pmid
    }
    
    # Try to extract the year from the publication date
    # pubdate might be "2024 Jan 15" or just "2024"
    pubdate = result["pubdate"]
    if pubdate and len(pubdate) >= 4:
        result["year"] = pubdate[:4]  # Take first 4 characters as year
    else:
        result["year"] = "Unknown"
    
    return result

if __name__ == "__main__":
    # Test search
    print("Testing search...")
    pmids = search_pubmed("breast cancer", 3)
    print(f"Found PMIDs: {pmids}")
    
    # Test fetch
    print("\nTesting article fetch...")
    for pmid in pmids:
        article = fetch_article_details(pmid)
        print(f"\nPMID: {article['pmid']}")
        print(f"Title: {article['title']}")
        print(f"Journal: {article['source']}")
        print(f"Year: {article['year']}")


REQUEST_DELAY = 0.35
def rate_limited_request(url,params):
    """Make a request and wait to respect rate limits"""
    response = requests.get(url, params=params)
    time.sleep(REQUEST_DELAY)  # Pause before next request
    return response