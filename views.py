from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
import urllib,logging, random,re
from django.shortcuts import render_to_response
from google.appengine.ext import db
from django.template import Context, loader
from sites import *
from feed import Feed 

def htmlSource(request):
  sites = ['FourChan', 'Fukung', 'Senorgif', 'Knowyourmeme' ]
  random.shuffle(sites)
  images = [] 
  images = globals()[sites[0]]().do().images()
  while not images:
   random.shuffle(sites)
   images = globals()[sites[0]]().do().images() 
  random.shuffle(images)
  if not Feed.gql("WHERE url = :1", images[0]).fetch(1):
    feed = Feed()
    feed.url = images[0]
    feed.put()
  return render_to_response('boardTemplate.html', {'image' : images[0]})

def ajax(request):
  sock = urllib.urlopen(request.GET['url'])
  while  sock.geturl() == "http://www.4chan.org/" or sock.geturl() == "http://www.4chan.org/banned":
    sock.close()
    sock = urllib.urlopen(request.GET['url'])
  img = sock.read()
  sock.close()
  return HttpResponse(img, mimetype="image/jpg")

def rss(request):
  feeds = Feed.gql('ORDER BY date DESC LIMIT 10')
  t = loader.get_template('rss.xml')
  c = Context({'feeds' : feeds, 'date' : feeds.fetch(1)[0].date})
  return HttpResponse(t.render(c), mimetype="application/xml") 

def index(request):
  return render_to_response('index.html')

