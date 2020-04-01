from flask import Flask, render_template
from flask import request
import feedparser
import json
import urllib.request
import urllib


app = Flask(__name__)

#BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc', 'city': 'London, UK'}

@app.route("/")
def home():
    # get customized headlines, based on input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    # get customized weather based on user input or default 
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template('home.html', articles=articles, weather = weather)
    
    

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
    weather = get_weather("London,UK")
    print(feed['entries'][0])
 

    return render_template("home.html", articles=feed['entries'], weather=weather)

def get_weather(query):
    #api_url = http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=c78c90c716c38663bfd4971a4906dd66
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78c90c716c38663bfd4971a4906dd66'
    query =  urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather =  {"description":
                    parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"]
                    }
    return weather

"""
Pushing our code to the server
git add headlines.py
git add templates
git commit -m "with Jinja templates"
git push origin master
"""


if __name__ == "__main__":
    app.run(port=5000, debug=True)
