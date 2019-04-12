from flask import render_template
from chat import chatApp

@chatApp.route("/")
@chatApp.route("/chat", methods=['GET' , 'POST'])
def chat():
    return render_template('chat.html', title="Chat")
