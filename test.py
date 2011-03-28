import logging
import httplib
import json

def compare(arta, artb):
    ''' returns -1 if article a is newer than article b, 0 if they are equal, 1 if artible b is newer '''
    # set precedence levels for econds. minutes, hours and days (anything more than days will default to greatest precedence)
    pre = {'se':0,'mi':1,'ho':2,'da':3}
    agea = arta['postedAgo'].split(' ') ; ageb = artb['postedAgo'].split(' ')
    # check the seconds/minutes/hours/days first - if the are equal, return the lowest value
    return pre.get(agea[1][:2],4).__cmp__(pre.get(ageb[1][:2],4)) or int(agea[0]).__cmp__(int(ageb[0]))

def get_articles(last_update):
    hn = httplib.HTTPConnection('api.ihackernews.com')
    hn.request('GET','/page')
    r1 = hn.getresponse()
    if r1.status == 200:
        try:
            text = r1.read()
            article_dict = json.loads(text)
            articles = sorted([a_js for a_js in article_dict['items']], cmp=lambda x,y: compare(x,y))
            import pdb ; pdb.set_trace()
            if article_dict['cachedOnUTC'] != last_update:
                last_update = article_dict['cachedOnUTC']
                print "updated"
            print "%s" % (article_dict['cachedOnUTC'],)
        except Exception, e:
            logging.error('Failed to parse Json response: %s', e)
    else:
        logging.error('Failed to get article list: %s, %s', r1.status, r1.reason)
    return last_update

get_articles(None)
'''last_update = None
for i in range(10):
    last_update = get_articles(last_update)'''
