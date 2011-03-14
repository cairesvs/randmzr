class Feed(db.Model):
  url = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

