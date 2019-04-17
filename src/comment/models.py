from comment import commentDB
from werkzeug.security import generate_password_hash, check_password_hash

class Comment(commentDB.Model):
	id = commentDB.Column(commentDB.Integer, primary_key=True)
	commentText = commentDB.Column(commentDB.String(144), index=True)
	postID = commentDB.Column(commentDB.Integer)
	user = commentDB.Column(commentDB.String(64), index=True)

	def __repr__(self):
		return "<Comment {}, text = \"{}\" by user {}>".format(self.id, self.commentText, self.user)

	def serialize(self):
		return {
			"id": self.id,
			"commentText": self.commentText,
			"postID": self.postID,
			"user": self.user
		}		