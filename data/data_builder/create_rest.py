"""
    Create node list for restaurants
"""
import json

# load the data from the reviews
bids = set()
with open('edge.tsv') as dfile:
    dfile.readline() # skip the column name
    for line in dfile:
        line = line.strip().split('\t')
        if len(line) < 2:
            continue
        bids.add(line[1])

# load the buisiness data
with open('restaurant.tsv', 'w') as wfile:
    col_names = [
        'bid', 'name', 'stars', 'review_count', 'city', 'state',
        'address', 'postal_code', 'latitude', 'longitude', 'categories'
    ]
    wfile.write('\t'.join(col_names) + '\n')

    with open('/home/public_data/yelp/dataset/business.json') as dfile:
        for line in dfile:
            entity = json.loads(line)

            # filter out the data not in the sets
            if entity['business_id'] not in bids:
                continue

            entity_info = [
                entity['business_id'], entity['name'], entity['stars'],
                entity['review_count'], entity['city'], entity['state'],
                entity['address'], entity['postal_code'], entity['latitude'],
                entity['longitude'], entity['categories']
            ]

            # convert to strings
            entity_info = map(str, entity_info)

            wfile.write('\t'.join(entity_info) + '\n')
