from flask import Flask
import requests
import json
from yelp_utils import headers, yelp_url


app=Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'title': 'hey'})

@app.route('/summary/<location>')
def summary(location):
    num_ratings = 0
    sum_ratings = 0
    num_reviews = 0

    query = 'physical-therapist'
    limit = 50
    url = '{}?location={}&term={}&limit={}'.format(yelp_url, location, query, limit)

    r = requests.get(url, headers=headers)
    status = r.status_code
    businesses = json.loads(r.content)['businesses']

    if status != 200:
        raise Exception('An error occured from yelp response')

    for business in businesses:
        if business['rating']:
            num_ratings += 1
            sum_ratings += business['rating']
        if business['review_count']:
            num_reviews += business['review_count']

        data = {
            'number_of_physical_therapists': len(businesses),
            'total_with_ratings': num_ratings,
            'avg_rating': sum_ratings / num_ratings,
            'total_reviews': num_reviews
        }
        return json.dumps(data)

@app.route('/list/<location>')
def list(location):
    query = 'physical-therapist'
    limit = 50
    url = '{}?location={}&term={}&limit={}'.format(yelp_url, location, query, limit)
    r = requests.get(url, headers=headers)
    status = r.status_code
    if status != 200:
        raise Exception('An error occured retrieving data from yelp api')
    businesses = json.loads(r.content)['businesses']
    businesses_list = []

    for business in businesses:
        if business['rating']:
            business_info = {
                'name': business['name'],
                'rating': business['rating'],
                'reviews': business['review_count'],
                'address': business['location']
            }
            businesses_list.append(business_info)
    businesses_list = sorted(businesses_list, key=lambda business : business['rating'], reverse=True)
    return json.dumps(businesses_list)



app.run(port=3000, debug=True)