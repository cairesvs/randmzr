from django.http import HttpResponse
import urllib,logging, random,re
from django.shortcuts import render_to_response

def htmlSource(request):
  boards = ['sp','b','g','v','mu','lit','ic','x','co','vp']
  random.shuffle(boards)
  sock = urllib.urlopen("http://boards.4chan.org/" + boards[0])    
  usock = urllib.urlopen('http://boards.4chan.org/b')
  logging.debug("url %s", sock.geturl())
  i = 0
  marotao = sock.geturl() == "http://www.4chan.org/" or sock.geturl() == "http://www.4chan.org/banned"
  quotas = usock.geturl() == "http://www.4chan.org/" or usock.geturl() == "http://www.4chan.org/banned"
  while marotao and quotas:
    i += 1
    sock.close()
    usock.close()
    random.shuffle(boards)
    sock = urllib.urlopen("http://boards.4chan.org/" + boards[0] + "/" + str(i))
    usock = urllib.urlopen('htt://boards.4chan.org/b')
    logging.debug("url dentro do while 2 %s", sock.geturl())

  html = sock.read()
  quotesHtml = usock.read()
  sock.close()
  allImages = re.findall('<a href="(.*images.*)" target="_blank">',html) 
  realQuotes = re.findall('<blockquote>.*',quotesHtml)
  realImages = []
  for image in allImages:
    realImages.append(re.search('(http://images.*)', image).group(0))
  
  random.shuffle(realImages)
  random.shuffle(realQuotes)
  return render_to_response('boardTemplate.html', {'image' : realImages[0], 'quote' : realQuotes[0]})

def ajax(request):
  sock = urllib.urlopen(request.GET['url'])
  img = sock.read()
  sock.close()
  return HttpResponse(img, mimetype="image/jpg")

def index(request):
  return render_to_response('index.html')
