from garden.models import Garden
from flask import render_template, jsonify
from sqlalchemy import func
from garden import db
from sqlalchemy import func
from garden import app
@app.route("/")
@app.route("/garden", methods=['GET' , 'POST'])
def garden():
    gardenItems = Garden.query.all();

    return (render_template('garden.html', title="Garden",  gardenItems=gardenItems))

@app.route("/garden/<User_id>/vegetable", methods=['GET','POST'])
def vegetable(User_id):
    vegetableItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        vegetableItems.append(row.vegetable)
    vegetableCo = Garden.query.with_entities(Garden.vegetable, Garden.Img_id, func.count(Garden.vegetable)).group_by(Garden.vegetable).filter(Garden.User_id == User_id).all()
    #vegetableCo = Garden.query.with_entities(Garden.vegetable,func.count(Garden.vegetable)).group_by(Garden.vegetable).filter(Garden.User_id == User_id).all()

    return(render_template('vegetables.html',title="vegetables", vegCount = vegetableCo, vegItems = vegetableItems))

@app.route("/garden/<User_id>/fruits", methods=['GET','POST'])
def fruits(User_id):
    fruitItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        fruitItems.append(row.fruits)
    fruitsCount = Garden.query.with_entities(Garden.fruits, Garden.Img_id, func.count(Garden.fruits)).group_by(Garden.fruits).filter(Garden.User_id == User_id).all()
    #fruitsCount = Garden.query.with_entities(Garden.fruits,func.count(Garden.fruits)).group_by(Garden.fruits).filter(Garden.User_id == User_id).all()
    return (render_template('fruits.html', title="fruits",fruCount=fruitsCount, fruitItems=fruitItems))

@app.route("/garden/<User_id>/getVegetables", methods=['GET'])
def getVegetables(User_id):
    vegetableItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        vegetableItems.append(row.vegetable)
    vegetableCo = Garden.query.with_entities(Garden.vegetable, Garden.Img_id, func.count(Garden.vegetable)).group_by(Garden.vegetable).filter(Garden.User_id == User_id).all()
    #vegetableCo = Garden.query.with_entities(Garden.vegetable,func.count(Garden.vegetable)).group_by(Garden.vegetable).filter(Garden.User_id == User_id).all()
    print(vegetableCo)
    return jsonify(vegetableCo)

@app.route("/garden/<User_id>/getFruits", methods=['GET'])
def getFruits(User_id):
    fruitItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        fruitItems.append(row.fruits)
    fruitsCount = Garden.query.with_entities(Garden.fruits, Garden.Img_id, func.count(Garden.fruits)).group_by(Garden.fruits).filter(Garden.User_id == User_id).all()
    #fruitsCount = Garden.query.with_entities(Garden.fruits,func.count(Garden.fruits)).group_by(Garden.fruits).filter(Garden.User_id == User_id).all()
    return jsonify(fruitsCount)

@app.route("/garden/<User_id>/getHerbs", methods=['GET'])
def getHerbs(User_id):
    herbItems = []
    # for row in db.session.query(Garden).filter_by(User_id=User_id):
    #     herbItems.append(row.herbs)
    # herbsCount = Garden.query.with_entities(Garden.herbs, Garden.Img_id, func.count(Garden.herbs)).group_by(Garden.herbs).filter(Garden.User_id == User_id).all()
    #fruitsCount = Garden.query.with_entities(Garden.fruits,func.count(Garden.fruits)).group_by(Garden.fruits).filter(Garden.User_id == User_id).all()
    return jsonify([])
    # return jsonify(herbsCount)

