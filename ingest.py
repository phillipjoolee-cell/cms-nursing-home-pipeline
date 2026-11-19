import json, requests, os
url = 'https://data.cms.gov/provider-data/api/1/datastore/query/4pq5-n9py/0'
limit = 500
offset = 0
page = 0
rows_pulled = 0
api_count = 0

os.makedirs('data/raw', exist_ok=True)
while True:
    data = requests.get(url, params={'limit': limit, 'offset': offset}).json()
    if len(data['results']) == 0:
        break
    with open(f'data/raw/page_{page}.json', 'w') as f:
        json.dump(data, f)
    print(f'page {page}: {len(data["results"])} rows')
    page += 1
    offset += limit
    rows_pulled += len(data['results'])
    api_count = data['count']

print(data.keys())

# cms_certification_number_ccn if facility key
# every value is strings, remember to typecast
print(f'Ingested {page} pages of data from the CMS API.')
print (f'Rows Pulled: {rows_pulled}')
print(f'API count: {api_count}')
if api_count == rows_pulled:
    print(f'MATCH')
else:
    print(f'MISMATCH {abs(api_count - rows_pulled)}')
