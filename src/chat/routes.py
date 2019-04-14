from flask import render_template
from chat import chatApp

@chatApp.route("/")
@chatApp.route("/chat", methods=['GET' , 'POST'])
def chat():
    users = {"User1","User2","User3","User4","User5","User6","User7","User8","User9","User10"}
    return render_template('chat.html', title="Chat",  users=users)
