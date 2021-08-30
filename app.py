#Use flask to render a template redirecting to another URL
from flask import Flask, render_template, redirect, url_for

#Use pymongo to interact with the mongo database
from flask_pymongo import PyMongo

#Scraping code, to convert the jupyter notebook to python
import Scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#Tells python that the app will connect to mongo using a URI (uniform resource identifier)
#The URI is saying that the app can reach Mongo through the server using  port 27017 using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Define the route for the HTML page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Defines the route flask will be using
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = Scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

#Tell flask to run
if __name__ == "__main__":
    app.run()


    
