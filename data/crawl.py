import requests
from lxml import html
import re
import urllib
import os
import time
import sys

# pre-settings
url_prefix = 'https://www.yelp.com/user_details?userid='
headers = { 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', \
    'accept-Encoding':'gzip, deflate, br', \
    'accept-Language':'en-US,en;q=0.9', \
    'connection':'keep-alive', \
    'user-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36',#'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36' \ Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0
    'Cookie': 'Login Yelp and obtain from your Browser. The scraping process was through running three computers simultaneously for near 2 months. To prevent blocking you need to keep switching IPs every 5 hours.'
}

# read user id from the files within the same folder. Only keep the id files
id_dir = './uids/'
filelist = [filep for filep in os.listdir(id_dir) if filep.endswith('.txt')]
categories = [filep.split('.')[0] for filep in filelist]

# create data folder under categories
if not os.path.isdir('./categories/'):
    os.mkdir('./categories/')
for name in categories:
    if not os.path.isdir('./categories/' + name + '/'):
        os.mkdir('./categories/' + name + '/')
        os.mkdir('./categories/' + name + '/images/') # images

# loop through each user id file.
for idx, filep in enumerate(filelist):
    print('Crawling ' + categories[idx] + ' from Yelp.')
    cdir = './categories/' + categories[idx]
    # data file
    dfile = open(cdir + '/collected.tsv', 'a')
    # load finished uids
    collected_ids = set()
    with open(cdir + '/collected.tsv') as cfile:
        for line in cfile:
            collected_ids.add(line.split('\t')[0])

    with open(id_dir+filep) as id_file:
        for uidx, user_id in enumerate(id_file):
            user_id = user_id.strip()
            if len(user_id) < 5:
                continue
            if user_id in collected_ids:
                continue
            
            # start to collect data
            print('Crawling: ' + user_id)
            url = url_prefix + user_id
            response = requests.request(method='get', url=url, headers=headers)

            # check the return status
            if response.status_code == 404:
                dfile.write(user_id + '\tx\n')
                dfile.flush()
                collected_ids.add(user_id)
                continue
            if response.status_code == 200 and 'This user has been removed.' in response.text:
                dfile.write(user_id + '\tx\n')
                dfile.flush()
                collected_ids.add(user_id)
                continue 

            page = html.fromstring(response.content)

            # get profile images
            regex = re.compile('https://s3-media[23].fl.yelpcdn.com/photo/(.+?)/ls.jpg')
            image_list = []
            image_names = []
            it = re.finditer(regex, response.text)
            for match in it:
                image_list.append(match.group(0))
                image_names.append(match.group(1))
            # keep the top 5 images
            image_list = image_list[:5]
            image_names = image_names[:5]

            # get location
            location = page.xpath('//h3[@class="user-location alternate"]')
            if location:
                location = location[0].text
                location = location.strip()
                if len(location) < 2:
                    location = 'x'  # default value
            else:
                if len(image_list) > 0:
                    location = 'x'
                else:
                    sys.exit()

            # download image
            if len(image_list) > 0:
                if not os.path.isdir(cdir + '/images/'+user_id):
                    os.mkdir(cdir + '/images/'+user_id)
                for idx in range(len(image_list)):
                    urllib.request.urlretrieve(
                        image_list[idx], 
                        cdir + '/images/' + user_id + '/' + image_names[idx] + '.jpg')
            
            # write location into file
            dfile.write(user_id + '\t' + location + '\n')
            dfile.flush()
            collected_ids.add(user_id)
            
            # sleep 5 seconds
            time.sleep(2)
    dfile.flush()
    dfile.close()
