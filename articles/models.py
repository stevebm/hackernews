from django.db import models
import datetime

class HackerNews(models.Model):
    postedBy = models.CharField(max_length=255)
    postedAgo = models.CharField(max_length=100)
    postedDate = models.DateTimeField()
    id = models.IntegerField(primary_key=True)
    points = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(HackerNews, self).__init__(*args, **kwargs)
        datekwargs = self.postedAgo.split(' ')
        if datekwargs[1][-1] != 's':
            datekwargs[1] += 's'
        datekwargs = {datekwargs[1]:int(datekwargs[0])}
        self.postedDate = datetime.datetime.now() - datetime.timedelta(**datekwargs)

    def __cmp__(self, other):
        ''' returns -1 if article a is newer than article b, 0 if they are equal, 1 if artible b is newer '''
        return other.postedDate.toordinal() - self.postedDate.toordinal()
        # set precedence levels for econds. minutes, hours and days (anything more than days will default to greatest precedence)
        # pre = {'se':0,'mi':1,'ho':2,'da':3}
        # ages = self.postedAgo.split(' ') ; ageo = other.postedAgo.split(' ')
        # check the seconds/minutes/hours/days first - if the are equal, return the lowest value
        # return pre.get(ages[1][:2],4) - pre.get(ageo[1][:2],4) or int(ages[0]) - int(ageo[0])

    def save(self):
        ''' do nothing because we don't need to write to the db '''
    def load(self):
        ''' do nothing '''
 
class Article(HackerNews):
    commentCount = models.IntegerField()
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

class ArtComment(HackerNews):
    comment = models.TextField()
    parentId = models.IntegerField()
    postId = models.IntegerField()

    def __init__(self,  *args, **kwargs):
        del kwargs['children']
        super(ArtComment, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.comment
