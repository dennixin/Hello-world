from flask import Flask, render_template
from flask import request
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
   return get_news()

@app.route("/cnn")
def cnn():
   return get_news()


@app.route("/", methods=['GET', 'POST'])

def get_news():
    #query = request.args.get("publication")
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    print(feed['entries'][0])
 

    return render_template("home.html", articles=feed['entries'])

"""
Pushing our code to the server
git add headlines.py
git add templates
git commit -m "with Jinja templates"
git push origin master
"""


if __name__ == "__main__":
    app.run(port=5000, debug=True)
