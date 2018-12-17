import json

# load the user_id from the geolocated user
uids_geo = dict()
with open('collected.tsv') as dfile:
    for line in dfile:
        line = line.strip().split('\t')
        if line[1] == 'x':
            continue
        uids_geo[line[0]] = line[1]

# load the user json and add the location to the user json
with open('user_geo.json', 'w') as wfile:
    with open('/home/public_data/yelp/dataset/user.json') as dfile:
        for line in dfile:
            entity = json.loads(line)
            if entity['user_id'] in uids_geo:
                entity['location'] = uids_geo[entity['user_id']]
                wfile.write(json.dumps(entity) + '\n')

# create user node file
with open('user.tsv', 'w') as wfile:
    # write column names of user tsv file
    col_names = [
        'uid', 'location', 'review_count', 'since',
        'friends', 'fans', 'average_stars'
    ]
    wfile.write(
        '\t'.join(col_names) + '\n'
    )
    with open('user_geo.json') as dfile:
        for line in dfile:
            entity = json.loads(line)
            entity_info = [
                entity['user_id'], entity['location'], str(entity['review_count']),
                entity['yelping_since'], str(len(entity['friends'])),
                str(entity['fans']), str(entity['average_stars'])
            ]
            wfile.write('\t'.join(entity_info) + '\n')
