from flask import Flask, render_template
import feedparser


app = Flask(__name__)

#BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/home")
def index():
   return "No news is good news!" 

@app.route("/")
@app.route("/bbc")
def bbc():
   return get_news('bbc')

@app.route("/cnn")
def cnn():
   return get_news('cnn')


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
 feed = feedparser.parse(RSS_FEEDS[publication])
 print(feed['entries'][0])
 #first_article = feed['entries'][0]
 #print(first_article)
#  return render_template("index.html",
#  title=first_article.get("title"),
#  published=first_article.get("published"),
#  summary=first_article.get("summary"))

# return render_template('home.html', article = first_article)
 #return render_template('home.html', articles = feed['entries'])
 return render_template("home.html", articles=feed['entries'])



if __name__ == "__main__":
    app.run(port=5000, debug=True)
