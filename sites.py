import urllib,logging, random,re
from BeautifulSoup import BeautifulSoup

class FourChan(object):
  def do(self):
    boards = ['i','b','an','ic','a','sp','g','v','mu','lit','ic','x','co','vp']
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
    try:
      return [fukung.find('img', {'class' : 'fukung'}).attrMap['src']]
    except Exception, e:
      return []

class Senorgif(object):
  def do(self):
    page = 'http://senorgif.memebase.com/page/' + str(random.randint(1,50))
    sock = urllib.urlopen(page) 
    self.html = sock.read()
    sock.close()
    return self

  def images(self):
    senorgif = BeautifulSoup(self.html)
    try:
      img = senorgif.findAll('img', {'class' : 'event-item-lol-image'})
      return [img[random.randint(1, 5)].attrMap['src']]
    except Exception, e:
      return []

class Knowyourmeme(object):
  def do(self):
    sock = urllib.urlopen('http://knowyourmeme.com/photos?page=' + str(random.randint(1,3000))) 
    self.html = sock.read()
    sock.close()
    return self

  def images(self):
    knowyourmeme = BeautifulSoup(self.html)
    try:
      section = knowyourmeme.find('section', id='photos')
      img = section.findAll('img', alt='')
      return [img[random.randint(1, 20)].attrMap['src'].replace('list', 'original')] 
    except Exception, e:
      return []


