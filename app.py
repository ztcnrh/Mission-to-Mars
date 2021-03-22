from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    # Find all records of data from the mongo database
    mars_data = mongo.db.mission_to_mars.find_one()
    # Return template and data
    return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mission_to_mars
    # Run the scrape function
    scraped_data = scrape_mars.scrape()
    # Update the Mongo database using the data scraped
    mongo.db.mission_to_mars.update({}, scraped_data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

