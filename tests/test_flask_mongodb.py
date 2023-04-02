from flask import Flask, render_template
from flask_pymongo import PyMongo
# mongosh "mongodb://mongo:CgBYQwt2TYtnxHArROFD@containers-us-west-32.railway.app:5746"
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/')
def home_page():
    online_users = mongo.db.users.find({'online': True})
    return render_template('index.html', online_users=online_users)