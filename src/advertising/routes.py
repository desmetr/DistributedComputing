from advertising.models import Advertisement
from advertising import advApp
from advertising import advDB
from flask import render_template, jsonify
from sqlalchemy import func
import base64
import json
from flask import send_file
import urllib.request

@advApp.route("/")
def advertisement():
    #print(Advertisement.query.delete())
    #advDB.session.commit()

    contents = json.loads(urllib.request.urlopen("http://127.0.0.1:5002/getRecentPosts/test").read().decode('utf-8'))
    bagOfWords = {}
    tags = Advertisement.query.with_entities(Advertisement.tag).distinct().all()
    totalAmountOfWords=0
    for tag in tags:
        bagOfWords[tag[0]]=0
    for post in contents:
        for word in str(post["postText"]).split():
            print("Looking at: " + word)
            word = word.replace(",","")
            word = word.replace(".","")
            word = word.replace("?","")
            word = word.replace("!","")
            word = word.replace(")","")
            word = word.replace("(","")
            word = word.replace("[","")
            word = word.replace("]","")
            word = word.replace("{","")
            word = word.replace("}","")
            if word.lower() in bagOfWords:
                bagOfWords[word.lower()] += 1
                totalAmountOfWords+=1
    #print(bagOfWords)
    #print(contents)
    advertisementJson={}
    for key in bagOfWords.keys():
        amountOfAds=int((float(bagOfWords[key])/float(totalAmountOfWords))*5)
        if(amountOfAds>0):
            advertisements = Advertisement.query.filter(Advertisement.tag==str(key)).order_by(func.random()).limit(amountOfAds).all()
            for advertisement in advertisements:
                print (Advertisement.serialize(advertisement))
                advertisementJson["adv"+str(len(advertisementJson)+1)]=Advertisement.serialize(advertisement)
    print("AdvertisementJson:")
    print(advertisementJson)
    return json.dumps(advertisementJson)

@advApp.route("/addAdvertisement")
def addAdvertisement():
    advertisement = Advertisement(tag="Potatoes".lower(), text="Potatoes like you've never seen before!", source_url="https://en.wikipedia.org/wiki/Potato")
    advDB.session.add(advertisement)
    advDB.session.commit()
    return "Advertisement added!"