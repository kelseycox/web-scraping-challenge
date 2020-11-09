# Import Dependencies
import pymongo
import flask
import render_template
import redirect
import jsonify
import mars_scrape

app = Flask(__name__)

# PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


@app.route("/")
def index():

    # Find data from Mongo
    mars = mongo.db.collection.find_one()

    # Return template
    return render_template("index.html", mars=mars)


@app.route("/")
def scrape():

    # Scrape function
    mars_data = mars_scrape.scrape()

    # Update Mongo database
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
