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

    # Bulid a conditional to return a default value before data is scraped:
    if mars_data == None:
        return render_template("index.html", data={
            'news_title': 'Click the above Scrape button to get the latest news',
            'news_p': '',
            'news_link': '#',
            'featured_image_url': '',
            'mars_facts': '',
            'hemisphere_image_urls': [
                {'title': 'Scrape to get the image', 'image_url': ''},
                {'title': 'Scrape to get the image', 'image_url': ''},
                {'title': 'Scrape to get the image', 'image_url': ''},
                {'title': 'Scrape to get the image', 'image_url': ''}]
            })
    # If we already have data...
    else:
        # Return template and the scraped data
        return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mission_to_mars
    # Run the scrape function
    scraped_data = scrape_mars.scrape()
    # Update the Mongo database using the data scraped
    mars_data.update({}, scraped_data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

