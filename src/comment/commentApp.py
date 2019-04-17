from comment import commentApp, commentDB
from comment.models import Comment

@commentApp.shell_context_processor
def make_shell_context():
	return {'commentDB': commentDB, 'Comment': Comment}