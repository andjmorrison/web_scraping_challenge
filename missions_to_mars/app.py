from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

from resources import username, password, cluster

app = Flask(__name__)

#pymongo
mongo = PyMongo(app, uri=f"mongodb+srv://{username}:{password}@{cluster}")


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
