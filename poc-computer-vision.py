subscription_key = "GET-YOUR-OWN-API-KEY"
assert subscription_key

vision_base_url = "https://northeurope.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"

import requests

def post_image(image_url):
	print('Posting URL to Azure: ', image_url)
	headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
	params   = {'visualFeatures': 'Categories,Description,Color'}
	data     = {'url': image_url}
	response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
	response.raise_for_status()
	analysis = response.json()

	image_caption = analysis["description"]["captions"][0]["text"].capitalize()
	image_caption
	print(image_url, "\n", image_caption)

import requests, sys

def httpRequestGetContent(url):
    """Trying to fetch the response content
    Attributes: url, as for the URL to fetch
    """

    timeout_in_seconds = 30

    try:
        a = requests.get(url)

        return a.text
    except requests.exceptions.SSLError:
        if 'http://' in url: # trying the same URL over SSL/TLS
            print('Info: Trying SSL before giving up.')
            return httpRequestGetContent(url.replace('http://', 'https://'))
    except requests.exceptions.ConnectionError:
        print(
            'Connection error! Unfortunately the request for URL "{0}" failed.\nMessage:\n{1}'.format(url, sys.exc_info()[0]))
        pass
    except:
        print(
            'Error! Unfortunately the request for URL "{0}" either timed out or failed for other reason(s). The timeout is set to {1} seconds.\nMessage:\n{2}'.format(url, timeout_in_seconds, sys.exc_info()[0]))
        pass

from bs4 import BeautifulSoup
from urllib.parse import urlparse

rss_feed_url = "http://www.vgregion.se/Public/RssResult/FeedCombined/149801?name=Aktuellt"
rss_feed = httpRequestGetContent(rss_feed_url)
soup = BeautifulSoup(rss_feed, "html.parser")

# print(soup)
### Fetching URL:s from RSS feed
i = 1
for items in soup.find_all("item"):
	url = ""
	if "http" in items.contents[1]:
		url = items.contents[1]
	elif "http" in items.contents[2]:
		url = items.contents[2]

	print("Found an URL in the feed:\n{0}. {1}".format(i, url))
	i += 1
	
	another_soup = BeautifulSoup(httpRequestGetContent(url),"html.parser")

	found_image = 0
	for image in another_soup.find_all('img', src=True):
		if '.jpg' in image['src']:
			found_image += 1
			#print('{0}. {1}'.format(found_image, image['src']))

			### sends the first JPG to Azure API for computer vision
			if "http" in image["src"]:
				### scheme is explicitly stated in image URL
				post_image(image['src'])
			else:
				### making image URL based on feed address
				post_image('{0}://{1}/{2}'.format(urlparse(rss_feed_url).scheme, urlparse(rss_feed_url).netloc, image['src']))
			break