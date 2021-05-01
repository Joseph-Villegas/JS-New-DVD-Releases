from flask import Flask, jsonify
from scraper import scrape, search_by_week

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>DVD Release Dates API</h1> \
        <p>This API retrieves retail release schedules for DVDs by performing a web scrape</p> \
        <p>Source: https://www.dvdsreleasedates.com</p> \
        <p>(Upcoming) Try these endpoints: /this-week, /last-week, /next-week, /in-two-weeks, /all-weeks</p>"

if __name__ == "__main__":
    app.run()