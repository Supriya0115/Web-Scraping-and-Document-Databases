# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
# Use PyMongo to set up mongo connection; define db and collection

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
# mars_db is the database; mars_data is the collection

@app.route("/")
def index():

    # Find data
    mars_mission_data = mongo.db.mars_data.find_one()

    # return template and data
    return render_template("index.html", mars_mission_data=mars_mission_data)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_mission_data = scrape_mars.scrape()

    # Insert mars_mission_data into database
    mongo.db.mars_data.update({},mars_mission_data,upsert = True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
