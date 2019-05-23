from flask import render_template, request, jsonify
from chat import chatApp
from chat import chatDB
from chat.models import Chat, ChatHistory
from sqlalchemy import or_
import json
import urllib.request
from chat import urlsConfig
from datetime import datetime

current_user_id = ""

@chatApp.route("/")
@chatApp.route("/chat", methods=['GET' , 'POST'])
def chat():  
    global current_user_id
    
    print("Cookie:")
    print(request.cookies.get("currentSessionCookie"))  
    current_user_id = request.cookies.get("currentSessionCookie")
    users=[]
    friends = json.loads(urllib.request.urlopen(urlsConfig.URLS['users_url']).read().decode('utf-8'))
    for friend in friends:
        print(friend["id"]) 
    return render_template('chat.html', title="Chat",  users=friends)

@chatApp.route("/chat/<username1>/<username2>", methods=["GET"])
def getChatId(username1,username2):
    user1Chats=Chat.query.filter(or_(Chat.user1==username1,Chat.user2==username1)).all()
    print("User1Chats:")
    foundChat=None
    for chat in user1Chats:
        if chat.user1==username2:
            foundChat=chat.id
            break
        if chat.user2==username2:
            foundChat=chat.id
            break
    if foundChat is None:
        newChat = Chat(user1=username1,user2=username2)
        chatDB.session.add(newChat)
        chatDB.session.commit()
        user1Chats=Chat.query.filter(or_(Chat.user1==username1,Chat.user2==username1)).all()
        print("User1Chats:")
        for chat in user1Chats:
            if chat.user1==username2:
                foundChat=chat.id
                break
            if chat.user2==username2:
                foundChat=chat.id
                break

    messages = ChatHistory.query.filter(ChatHistory.chatID==foundChat).all()
    messagesJSON = "["
    for message in messages:
        messagesJSON+=ChatHistory.serialize(message)+","
    messagesJSON = messagesJSON[:-1]
    messagesJSON+="]"

    print("{{\"id\":\"{}\",\"messages\":{}}}".format(foundChat,messagesJSON))
    if len(messages)>0:
        return "{{\"id\":\"{}\",\"messages\":{}}}".format(foundChat,messagesJSON)
    else:
        return "{{\"id\":\"{}\"}}".format(foundChat)
@chatApp.route("/chatHistory/<chatID>",methods=["GET"])
def getChatHistory(chatID):
    messages = ChatHistory.query.filter(ChatHistory.chatID==chatID).all()
    print(messages)
    return "Getting mesages"

@chatApp.route("/chatHistory", methods=["POST"])
def addMessage():
    print("We got a post!")
    print(request.data.decode('utf-8'))
    decodedMessage=json.loads(request.data.decode('utf-8'))
    print(decodedMessage)
    ch = ChatHistory(chatID=decodedMessage["chatID"],timeStamp=datetime.strptime(decodedMessage["time"], '%Y-%m-%d %H:%M:%S'), message=decodedMessage["message"], userID=decodedMessage["userID"])
    chatDB.session.add(ch)
    chatDB.session.commit()
    return "Successfully added to history"

@chatApp.route("/chatHistory/getAll",methods=["GET"])
def getAllHistory():
    messages = ChatHistory.query.all()
    return jsonify([ChatHistory.serialize(message) for message in messages])

# Needed to redirect to urls of another service
@chatApp.route("/redirectToGarden", methods=["GET"])
def redirectToGarden():
    global current_user_id

    response = redirect(urlsConfig.URLS['garden_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@chatApp.route("/redirectToNewsfeed", methods=["GET"])
def redirectToNewsfeed():
    global current_user_id

    response = redirect(urlsConfig.URLS['newsfeed_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@chatApp.route("/redirectToPost", methods=["GET"])
def redirectToPost():
    global current_user_id

    response = redirect(urlsConfig.URLS['post_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@chatApp.route("/redirectToLocation", methods=["GET"])
def redirectToLocation():
    global current_user_id

    response = redirect(urlsConfig.URLS['location_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 


@chatApp.errorhandler(Exception)
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