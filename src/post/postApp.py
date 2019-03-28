from post import postApp, postDB
from post.models import Post

@postApp.shell_context_processor
def make_shell_context():
	return {'postDB': postDB, 'Post': Post}