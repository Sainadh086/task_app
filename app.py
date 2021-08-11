from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask("__main__",static_folder="templates/")

#connecting a mongodb
db = MongoClient("mongodb://127.0.0.1:27017")
notes = db['app']['notes']
# lambda function
p_data = lambda x: request.form.get(x)







@app.route("/", methods= ['GET', 'POST'])
def index():
    if request.method == "POST":
        title = p_data('title')
        desc = p_data('description')
        status = p_data('status')
        operation = p_data('operation')
        id = p_data('id')
        if operation == 'create':
            notes.insert({'title':title, 'description':desc, 'status':status})
        elif operation == 'update':
            notes.update_one({'_id':ObjectId(id)},{'$set' :{'title':title,'description':desc,'status':status}})
        elif operation == 'remove':
            print("*"*10)
            print(id)
            notes.delete_one({'_id':ObjectId(id)})
        elif operation == 'edit':
            data = notes.find({"_id": ObjectId(id) })
            return render_template('edit.html', note = data[0])
        else:
            pass
    data = notes.find()
    return render_template("index.html",notes=data )

@app.route("/create")
def create():
    return render_template("create.html")

if __name__ =="__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
