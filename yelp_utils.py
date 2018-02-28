from keys import yelp_key

yelp_url = 'https://api.yelp.com/v3/businesses/search'

headers = {
    'Authorization': 'Bearer {}'.format(yelp_key)
}

