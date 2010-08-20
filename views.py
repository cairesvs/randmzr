from django.http import HttpResponse
import urllib,logging, random,re
from django.shortcuts import render_to_response

def htmlSource(request):
  boards = ['r','s','sp','b','g','v','mu','lit','ic','x','co','vp']
  random.shuffle(boards)
  sock = urllib.urlopen("http://boards.4chan.org/" + boards[0])    
  logging.info("url %s", sock.geturl())
  i = 0
  while sock.geturl() == "http://www.4chan.org/" or sock.geturl() == "http://www.4chan.org/banned":
    i += 1
    sock.close()
    random.shuffle(boards)
    sock = urllib.urlopen("http://boards.4chan.org/" + boards[0] + "/" + str(i))
    logging.info("url dentro do while 2 %s", sock.geturl())

  usock = urllib.urlopen('http://boards.4chan.org/b')
  while usock.geturl() == "http://www.4chan.org/" or usock.geturl() == "http://www.4chan.org/banned":
    usock.close()
    usock = urllib.urlopen('http://boards.4chan.org/b')

  html = sock.read()
  quotesHtml = usock.read()
  sock.close()
  allImages = re.findall('<a href="(.*images.*)" target="_blank">',html) 
  realQuotes = re.findall('<blockquote>.*',quotesHtml)
  logging.info("images all %s", allImages)
  logging.info("quotes real %s",realQuotes)
  realImages = [re.search('(http://images.*)', image).group(0) for image in allImages]
  random.shuffle(realImages)
  random.shuffle(realQuotes)
  logging.info("images %s", realImages)
  logging.info("quotes %s",realQuotes)
  return render_to_response('boardTemplate.html', {'image' : realImages[0], 'quote' : realQuotes[0]})

def ajax(request):
  sock = urllib.urlopen(request.GET['url'])
  while  sock.geturl() == "http://www.4chan.org/" or sock.geturl() == "http://www.4chan.org/banned":
    sock.close()
    sock = urllib.urlopen(request.GET['url'])

  img = sock.read()
  sock.close()
  return HttpResponse(img, mimetype="image/jpg")

def index(request):
  return render_to_response('index.html')
