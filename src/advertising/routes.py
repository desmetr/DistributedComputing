from advertising.models import Advertisement
from advertising import advApp
from advertising import advDB
from flask import render_template, jsonify, request
from sqlalchemy import func
import json
from flask import send_file
import urllib.request
from advertising import urlsConfig
import base64
from advertising.forms import AdvertisementForm
import requests

@advApp.route("/getAdvertisements/<userId>")
def advertisement(userId):
    #print(Advertisement.query.delete())
    #advDB.session.commit()
    print("made it to advertisements")
    print(Advertisement.query.all())

    contents = json.loads(urllib.request.urlopen(urlsConfig.URLS['all_posts_for_user_url']+"/"+userId).read().decode('utf-8'))
    bagOfWords = {}
    tags = Advertisement.query.with_entities(Advertisement.tag).distinct().all()
    print("tags")
    print(tags)
    totalAmountOfWords=0
    for tag in tags:
        bagOfWords[tag[0]]=0
    print(bagOfWords)
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
    if totalAmountOfWords>0:
        advertisementJson=[]
        for key in bagOfWords.keys():
            amountOfAds=int((float(bagOfWords[key])/float(totalAmountOfWords))*5)
            if(amountOfAds>0):
                advertisements = Advertisement.query.filter(Advertisement.tag==str(key)).order_by(func.random()).limit(amountOfAds).all()
                for advertisement in advertisements:
                    print (Advertisement.serialize(advertisement))
                    advertisementJson.append(Advertisement.serialize(advertisement))
        print("AdvertisementJson:")
        print(advertisementJson)
        return json.dumps(advertisementJson)
    else:
        return "{}"

@advApp.route("/getAllAdvertisements", methods=["GET", "POST"])
def getAllAdvertisement():
    advertisementsJson = [Advertisement.serialize(adv) for adv in Advertisement.query.all()]
    return json.dumps(advertisementsJson)

@advApp.route("/advertisement",  methods=["GET", "POST"])
def addAdvertisement():
    global current_user_id
    current_user_id = request.cookies.get("currentSessionCookie")
    if current_user_id:
        # Get current user information
        print(current_user_id)
        current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))

        if current_user_response.status_code == 200:
            adForm = AdvertisementForm()
            print("Checking form")
            if adForm.validate_on_submit():
                print("valid")
                print(adForm.image.data)
                newAd = Advertisement(tag=str(adForm.tag.data).lower(),text=adForm.advertisementText.data,source_url=adForm.source.data,img=base64.b64encode(adForm.image.data.read()).decode('utf-8'))
                advDB.session.add(newAd)
                advDB.session.commit()
                return "Ad has been added correctly!"
                
            return render_template("advertising.html", title="Advertisement", adForm=adForm)
        else:
            return redirect(urlsConfig.URLS['login_url'])
    else:
        return redirect(urlsConfig.URLS['login_url'])

    #img=""
    #with open("static/img/Growing-Potatoes-Commercially.png", "rb") as image_file:
    #    img= base64.b64encode(image_file.read()).decode('utf-8')
    #advertisement = Advertisement(tag="Potatoes".lower(), text="Potatoes like you've never seen before!", source_url="https://en.wikipedia.org/wiki/Potato",img=img)
    #advDB.session.add(advertisement)
    #advDB.session.commit()
    #return "Advertisement added!"


@advApp.route("/deleteAdvertisement", methods=['GET', 'POST', 'DELETE'])
def deleteAdverstiment():
    adv_id = int(request.args.get('adv_id'))
    advertisement = Advertisement.query.filter_by(id=adv_id).delete()
    advDB.session.commit()
    return "OK"

# @advApp.errorhandler(Exception)
# def exceptionHandler(error):
#     print(error)
#     errorString = "Something went wrong! It seems there was a " + error.__class__.__name__ + " while making a request"
#     if "post" in repr(error).lower():
#         errorString += " to the Post service."
#     elif "comment" in repr(error).lower():
#         errorString += " to the Comment service."
#     elif "photo" in repr(error).lower():
#         errorString += " to the Photo service."
#     elif "advertisements" in repr(error).lower():
#         errorString += " to the Advertisement service."
#     elif "user" in repr(error).lower():
#         errorString += " to the Login service."
#     elif "location" in repr(error).lower():
#         errorString += " to the Location service."
#     else:
#         errorString += "."
#     return errorString