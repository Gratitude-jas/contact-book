from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.contact_book
contacts_collection = db.contacts

@app.route('/')
def index():
    search_query = request.args.get('search')
    if search_query:
        contacts = list(contacts_collection.find({'name': {'$regex': search_query, '$options': 'i'}}))
    else:
        contacts = list(contacts_collection.find())
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')

    if name and phone:
        contacts_collection.insert_one({'name': name, 'phone': phone})

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
