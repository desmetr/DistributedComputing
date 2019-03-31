from garden.models import Garden
from flask import render_template
from garden import app

@app.route("/")
@app.route("/garden", methods=['GET' , 'POST'])
def garden():
    gardenItems = Garden.query.all();
    return render_template('garden.html', title="Garden",  gardenItems=gardenItems)

@app.route("/garden/vegetable", methods=['GET','POST'])
def vegetable():
    vegetableItems = Garden.query.filter_by(item_type='vegetable').all()
    return render_template('vegetables.html', title="vegetable", vegetableItems=vegetableItems)


@app.route("/garden/fruits", methods=['GET','POST'])
def fruits():
    fruitItems = Garden.query.filter_by(item_type='fruits').all()
    return render_template('fruits.html', title="fruits", fruitItems=fruitItems)
