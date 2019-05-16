from flask import render_template
from chat import chatApp
from chat import chatDB
from chat.models import Chat
from sqlalchemy import or_

@chatApp.route("/")
@chatApp.route("/chat", methods=['GET' , 'POST'])
def chat():      
    users = {"User1","b","c","User4","User5","User6","User7","User8","User9","User10"}
    return render_template('chat.html', title="Chat",  users=users)

@chatApp.route("/chat/<username1>/<username2>")
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
    return "{{\"id\": \"{}\"}}".format(foundChat)