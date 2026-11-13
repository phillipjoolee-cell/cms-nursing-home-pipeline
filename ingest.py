import json, requests, os
url = 'https://data.cms.gov/provider-data/api/1/datastore/query/4pq5-n9py/0'
limit = 500
offset = 0
page = 0

os.makedirs('data/raw', exist_ok=True)
while True:
    data = requests.get(url, params={'limit': limit, 'offset': offset}).json()
    if len(data['results']) == 0:
        break
    with open(f'data/raw/page_{page}.json', 'w') as f:
        json.dump(data, f)
    page += 1
    offset += limit

# cms_certification_number_ccn if facility key
# every value is strings, remember to typecast
print(f'Ingested {page} pages of data from the CMS API.')