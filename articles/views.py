from articles.models import Article, ArtComment
from django.http import HttpResponse
from django.shortcuts import render_to_response
import httplib
import json
import logging

def get_data(data_type='article', category='new'):
    if data_type == 'article' and category not in ['new','page']:
        logging.error("Category must be 'new' or 'page' (for front page articles)")
        return []
    hn = httplib.HTTPConnection('api.ihackernews.com')
    # get the endpoint for the api query
    path = category if data_type == 'article' else 'newcomments'
    hn.request('GET','/'+path)
    r1 = hn.getresponse()
    if r1.status == 200:
        try:
            text = r1.read()
            data_dict = json.loads(text)
        except Exception, e:
            logging.error('Failed to parse Json response: %s', e)
            return []
        # get the list of either comments or articles based on data_type
        if data_type == 'article':
            if category == 'new':
                data_dict['items'] = data_dict['items'][:5]
            data_list = [Article(**i) for i in data_dict['items']]
        else:
            data_list = [ArtComment(**i) for i in data_dict['comments'][:5]]
        if data_type != 'article' or  category == 'new':
            # list is already sorted
            return (True,data_list[:5])
        else:
            # need to sort to find the newest front page articles
            return (True,sorted(data_list)[:5])
    else:
        logging.error('Failed to get %s list: %s, %s', data_type, r1.status, r1.reason)
        return (False,r1)

def index(request):
    new_articles = get_data()
    #front_page_articles = get_data(category='page')
    comments = get_data(data_type='comments')
    return render_to_response('index.html', {
        'asuccess':new_articles[0],
        'articles':new_articles[1],
        'csuccess':comments[0],
        'comments':comments[1]})

def detail(request, article_id):
    return HttpResponse("You're looking at article %s." % article_id)
