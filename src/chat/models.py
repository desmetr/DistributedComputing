#To hold database model
from chat import chatDB
from datetime import datetime
import json
class Chat(chatDB.Model):
    #__tablename__ = 'chats'
    id=chatDB.Column(chatDB.Integer, primary_key=True)
    user1=chatDB.Column(chatDB.String)
    user2=chatDB.Column(chatDB.String)

    def __repr__(self):
        return f"chat('{self.id}','{self.user1}','{self.user2}')"

class ChatHistory(chatDB.Model):
    id=chatDB.Column(chatDB.Integer, primary_key=True)
    chatID=chatDB.Column(chatDB.Integer,nullable=False)
    timeStamp=chatDB.Column(chatDB.DateTime, nullable=False)
    message=chatDB.Column(chatDB.String,nullable=False)
    userID=chatDB.Column(chatDB.Integer,nullable=False)
    
    def serialize(self):
        return json.dumps({
            "id": self.id,
            "chatID": self.chatID,
            "timeStamp": str(self.timeStamp),
            "message": self.message,
            "userID": self.userID
        })