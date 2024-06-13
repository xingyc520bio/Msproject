import requests
from datetime import datetime, timedelta

db = "nucleotide"
term = "Enterovirus D68[Organism]"
rettype = "xml"
retmode = "xml"
tool = "xingyc0714@gmail.com"

two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
date_range = f"filter=sdate:{two_years_ago}-to-{datetime.now().strftime('%Y-%m-%d')}"

search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={term}&rettype={rettype}&retmode={retmode}&daterange={date_range}&usehistory=y&tool={tool}"

response = requests.get(search_url)

if response.status_code == 200:
   xml_response = response.text
   print(xml_response)
else:
   print("Failed to retrieve data:", response.status_code)
