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
#uses Pymongo to find the "mars" collection in the database.
#return render: tells flask to return an HTML template using an index.html file
#mars=mars, tells python to use the "mars" collection in MongoDB
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Defines the route flask will be using
@app.route("/scrape")
#defining the function scrape
def scrape():
   #variable that points to the mongo database
   mars = mongo.db.mars
   #New variable to hold the scraped data 
   mars_data = Scraping.scrape_all()
   #update the database
   mars.update({}, mars_data, upsert=True)
   #add a redirect after succesfully scraping the data
   return redirect('/', code=302)

#Tell flask to run
if __name__ == "__main__":
    app.run()


    
