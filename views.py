from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
import urllib,logging, random,re
from django.shortcuts import render_to_response

def htmlSource(request):
  chan = FourChan()
  fukung = Fukung()
  senorgif = Senorgif()
  realImages = []
  realImages = chan.do().images() + fukung.do().images() + senorgif.do().images() 
  random.shuffle(realImages)
  return render_to_response('boardTemplate.html', {'image' : realImages[0]})

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

class FourChan(object):
  def do(self):
    boards = ['sp','b','g','v','mu','lit','ic','x','co','vp']
    random.shuffle(boards)
    sock = urllib.urlopen("http://boards.4chan.org/" + boards[0])    
    i = 0
    while sock.geturl() == "http://www.4chan.org/" or sock.geturl() == "http://www.4chan.org/banned":
      i += 1
      sock.close()
      random.shuffle(boards)
      sock = urllib.urlopen("http://boards.4chan.org/" + boards[0] + "/" + str(i))

    self.html = sock.read()
    sock.close()
    return self

  def images(self):
    chan = self
    chan_html = BeautifulSoup(chan.html)
    allAnchors = chan_html.findAll('a', target = '_blank')
    fourChanImages = []
    for anchor in allAnchors:
      if re.search('images', anchor.attrMap['href']):
        fourChanImages.append(anchor.attrMap['href'])
    random.shuffle(fourChanImages)
    return [fourChanImages[0]]

class Fukung(object):
  def do(self):
    sock = urllib.urlopen('http://fukung.net/random')    
    self.html = sock.read()
    sock.close()
    return self
    
  def images(self):
    fukung = BeautifulSoup(self.html)
    return [fukung.findAll('img', {'class' : 'fukung'})[0].attrMap['src']]

class Senorgif(object):
  def do(self):
    sock = urllib.urlopen('http://senorgif.memebase.com/page/' + str(random.randint(1,50))) 
    self.html = sock.read()
    sock.close()
    return self

  def images(self):
    senorgif = BeautifulSoup(self.html)
    return [senorgif.findAll('img', {'class' : 'event-item-lol-image'})[0].attrMap['src']]
