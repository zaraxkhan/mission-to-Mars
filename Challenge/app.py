from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

 


# Connect to Mongo with Pymongo
app = Flask(__name__)
app.config["MONGO_URI"]=("mongodb://localhost:27017/mars_app")
mongo=PyMongo(app)

# Define HTML route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#Next route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# Tell flask to run
if __name__ == "__main__":
   app.run()
