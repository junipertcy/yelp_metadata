import json
"""
    uid: user id
    bid: buisiness id
    eid: edge id == review id
    stars: review scores
    date: 
"""

def process_text(text):
    text = text.replace('\t', ' ')
    text = text.replace('\n', ' ')
    return text


# load the data from the user tsv file
uids = set()
with open('user.tsv') as dfile:
    dfile.readline() # skip the column name
    for line in dfile:
        line = line.strip().split('\t')
        if len(line) < 1:
            continue
        uids.add(line[0])

# load the business ids are in restaurants or food
bids = set()
with open('/home/public_data/yelp/dataset/business.json') as dfile:
    for line in dfile:
        entity = json.loads(line)

        if 'Restaurants' in entity['categories']: # 'Food' in entity['categories'] or 
            bids.add(entity['business_id'])

# load the reviews data
# only keep existing users?
with open('edge.tsv', 'w') as wfile:
    col_names = [
        'uid', 'bid', 'eid', 'stars', 'date',
        'text', 'useful', 'funny', 'cool'
    ]
    wfile.write('\t'.join(col_names) + '\n')
    with open('/home/public_data/yelp/dataset/review.json') as dfile:
        for line in dfile:
            entity = json.loads(line)

            # filter out un-collected users
            if entity['user_id'] not in uids:
                continue
            if entity['business_id'] not in bids:
                continue

            entity_info = [
                entity['user_id'], entity['business_id'], 
                entity['review_id'], str(entity['stars']), entity['date'], 
                process_text(entity['text']), str(entity['useful']), 
                str(entity['funny']), str(entity['cool']),
            ]
            entity_str = '\t'.join(entity_info)
            wfile.write(entity_str + '\n')
