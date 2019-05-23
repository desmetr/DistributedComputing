from garden.models import Garden
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests
import urllib.request
from garden import urlsConfig
from flask import render_template, jsonify, flash, redirect, url_for, jsonify, request
from garden.forms import GroceryForm
from garden import db
from sqlalchemy import func
from garden import app

current_user_id = ""

@app.route("/")
@app.route("/garden", methods=['GET', 'POST'])
def garden():
    global current_user_id
    current_user_id = request.cookies.get("currentSessionCookie")
    if current_user_id:
        # Get current user information
        print(current_user_id)
        current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))

        if current_user_response.status_code == 200:
            gardenItems = Garden.query.all();

            return (render_template('garden.html', title="Garden",  gardenItems=gardenItems))
        else:
            return redirect(urlsConfig.URLS['login_url'])
    else:
        return redirect(urlsConfig.URLS['login_url'])

#Display under Garden page, Prints all veggies in db (no user specific)
@app.route("/garden/vegetable", methods=['GET','POST'])
def vegetable():
    vegetableCo = Garden.query.with_entities(Garden.vegetable, Garden.Img_id, func.count(Garden.vegetable)).group_by(Garden.vegetable).all()
    return(render_template('vegetables.html',title="vegetables", vegCount = vegetableCo))

@app.route("/garden/fruits", methods=['GET','POST'])
def fruits():
    fruitsCount = Garden.query.with_entities(Garden.fruits, Garden.Img_id, func.count(Garden.fruits)).group_by(Garden.fruits).all()
    return (render_template('fruits.html', title="fruits",fruCount=fruitsCount))

@app.route("/garden/herbs", methods=['GET','POST'])
def herbs():
    herbCount = Garden.query.with_entities(Garden.herbs, Garden.Img_id, func.count(Garden.herbs)).group_by(Garden.herbs).all()
    return (render_template('herbs.html', title="herbs", herbCount=herbCount))

# FOR KEERTHANA: change this to showVegetables that only shows the vegetables of a user and do the same for fruits and herbs
#This is the garden page we will have bar for veg,herb,fruits for that user
@app.route("/garden/showGarden", methods=['GET','POST'])
def showGarden():
    global current_user_id

    current_user_id = request.cookies.get("currentSessionCookie")
    if current_user_id:
        # Get current user information
        current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))
        if current_user_response.status_code == 200:
            vegetablesItems = []
            for row in db.session.query(Garden).filter_by(User_id=current_user_id):
                vegetablesItems.append(row.vegetable)
            fruitsItems = []
            for row in db.session.query(Garden).filter_by(User_id=current_user_id):
                fruitsItems.append(row.fruits)
            herbsItems = []
            for row in db.session.query(Garden).filter_by(User_id=current_user_id):
                herbsItems.append(row.herbs)
            return (render_template('garden.html',vegetableitem=vegetablesItems, fruitsitem=fruitsItems, herbitem=herbsItems))
        else:
            return redirect(urlsConfig.URLS['login_url'])
    else:
        return redirect(urlsConfig.URLS['login_url'])

@app.route("/garden/<User_id>/getVegetables", methods=['GET','POST'])
def getVegetables(User_id):
    vegetablesItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        vegetablesItems.append(row.vegetable)
    vegetablesCount = Garden.query.with_entities(Garden.vegetable, Garden.Img_id, func.count(Garden.vegetable)).group_by(Garden.vegetable).filter(Garden.User_id == User_id).all()
    print(vegetablesItems)
    return jsonify(vegetablesItems)

@app.route("/garden/<User_id>/getFruits", methods=['GET','POST'])
def getFruits(User_id):
    fruitsItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        fruitsItems.append(row.fruits)
    fruitsCount = Garden.query.with_entities(Garden.fruits, Garden.Img_id, func.count(Garden.fruits)).group_by(Garden.fruits).filter(Garden.User_id == User_id).all()
    return jsonify(fruitsItems)

@app.route("/garden/<User_id>/getHerbs", methods=['GET','POST'])
def getHerbs(User_id):
    herbsItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        herbsItems.append(row.herbs)
    herbsCount = Garden.query.with_entities(Garden.herbs, Garden.Img_id, func.count(Garden.herbs)).group_by(Garden.herbs).filter(Garden.User_id == User_id).all()
    return jsonify(herbsItems)

@app.route("/AddGrocery", methods=['GET', 'POST'])
def AddGrocery():
    global current_user_id

    current_user_id = request.cookies.get("currentSessionCookie")
    if current_user_id:
        # Get current user information
        current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))
        if current_user_response.status_code == 200:
            groceryForm = GroceryForm()
            print(groceryForm)
            if groceryForm.validate_on_submit():
        #flash('Successfully add the grocery list')

                user= Garden(User_id=current_user_id,vegetable=groceryForm.vegetable.data, fruits=groceryForm.fruits.data, herbs=groceryForm.herbs.data)
                db.session.add(user)
                db.session.commit()
                flash(f'Added grocery ','success')
                return redirect(url_for("garden"))
            return render_template('AddGrocery.html', title="AddGrocery", form = groceryForm)
        else:
            return redirect(urlsConfig.URLS['login_url'])
    else:
        return redirect(urlsConfig.URLS['login_url'])


# Needed to redirect to urls of another service
@app.route("/redirectToNewsfeed", methods=["GET"])
def redirectToNewsfeed():
    global current_user_id

    response = redirect(urlsConfig.URLS['newsfeed_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToChat",methods=["GET"])
def redirectToChat():
    global current_user_id

    response = redirect(urlsConfig.URLS['chat_url'])
    print("setting cookie:" + current_user_id)
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToPost", methods=["GET"])
def redirectToPost():
    global current_user_id

    response = redirect(urlsConfig.URLS['post_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToLocation", methods=["GET"])
def redirectToLocation():
    global current_user_id

    response = redirect(urlsConfig.URLS['location_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 


@app.errorhandler(Exception)
def exceptionHandler(error):
    print(error)
    errorString = "Something went wrong! It seems there was a " + error.__class__.__name__ + " while making a request"
    if "post" in repr(error).lower():
        errorString += " to the Post service."
    elif "comment" in repr(error).lower():
        errorString += " to the Comment service."
    elif "photo" in repr(error).lower():
        errorString += " to the Photo service."
    elif "advertisements" in repr(error).lower():
        errorString += " to the Advertisement service."
    elif "user" in repr(error).lower():
        errorString += " to the Login service."
    elif "location" in repr(error).lower():
        errorString += " to the Location service."
    else:
        errorString += "."
    return errorString