from flask import Flask, render_template, redirect
import pymongo

app = Flask(__name__)

# Connect to MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to the mars_app database
db = client.mars_app

# Connect to mars collection 
mars_coll = db.mars
    
@app.route('/')
def index():

    mars_data = mars_coll.find_one()

    return(render_template('index.html', mars_data=mars_data))

@app.route('/scrape')
def scrape():
    
    import scrape_mars

    # Gather document to insert
    nasa_document = scrape_mars.scrape_all()

    # Insert into the mars collection
    # mars.insert_one(data_document)

    # Upsert into database (preferred to avoid duplicates)
    mars_coll.update_one({}, {'$set': nasa_document}, upsert=True)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
